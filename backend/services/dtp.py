import csv
import io
import pandas as pd
from datetime import datetime, timezone
from typing import Optional

from db.connection import get_connection
from entity.daily_record import DailyRecord
from entity.raw_dtp_record import DTP_COLUMNS, RawDtpRecord
from entity.load_log_record import LoadLogRecord
from services.utils import fetch_page
from services.weather import enqueue_months


DTP_INSERT_SQL = (
    f"INSERT INTO raw_dtp ({', '.join(DTP_COLUMNS)}) "
    f"VALUES ({', '.join(f'%({c})s' for c in DTP_COLUMNS)}) "
    "ON CONFLICT (id) DO NOTHING"
)

MAX_PAGE_SIZE = 500


def _write_log(file_name: str, started_at: datetime, status: str, rows_total: int = 0, rows_inserted: int = 0, error: Optional[str] = None) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO dtp_load_log
                (file_name, started_at, finished_at, status,
                 rows_total, rows_inserted, error)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                file_name,
                started_at,
                datetime.now(timezone.utc),
                status,
                rows_total,
                rows_inserted,
                error,
            ),
        )

def _months_from_dtp(conn) -> set[tuple[int, int]]:
    with conn.cursor() as cur:
        cur.execute("""
            WITH r AS (
                SELECT date_trunc('month', MIN(datetime)) AS lo,
                       date_trunc('month', MAX(datetime)) AS hi
                FROM raw_dtp
            )
            SELECT EXTRACT(YEAR FROM g)::int,
                   EXTRACT(MONTH FROM g)::int
            FROM r,
                 generate_series(r.lo, r.hi, interval '1 month') AS g
        """)
        return set(cur.fetchall())


def import_dtp(content: bytes, file_name: str) -> int:
    started_at = datetime.now(timezone.utc)

    try:
        text = content.decode("utf-8-sig")
        records = [
            RawDtpRecord.from_csv_row(row)
            for row in csv.DictReader(io.StringIO(text))
        ]

        if not records:
            _write_log(file_name, started_at, "empty")
            return 0

        with get_connection() as conn, conn.cursor() as cur:
            cur.executemany(DTP_INSERT_SQL, [r.to_params() for r in records])
            inserted = cur.rowcount

        _write_log(
            file_name, started_at, "ok",
            rows_total=len(records), rows_inserted=inserted,
        )

        with get_connection() as conn:
            needed = _months_from_dtp(conn)
            enqueue_months(conn, station_id=27612, months=needed)
            _update_daily(conn)

        return inserted

    except Exception as e:
        _write_log(file_name, started_at, "error", error=str(e)[:1000])
        raise


def get_raw_dtp(page: int = 1, page_size: int = 500) -> dict:
    return fetch_page(RawDtpRecord, "raw_dtp", "datetime DESC, id", page, page_size)

def get_daily(page: int = 1, page_size: int = 500) -> dict:
    return fetch_page(DailyRecord, "daily", "date DESC", page, page_size)

def get_load_log(page: int = 1) -> dict:
    return fetch_page(LoadLogRecord, "dtp_load_log", "started_at DESC, id DESC", page, 500)

def _update_daily(conn) -> None:
    # Читаем все записи ДТП и превращаем их в DataFrame
    result = get_raw_dtp(1, -1)
    df = pd.DataFrame(result["items"])
    if df.empty:
        return
    if df.empty:
        return

    # Оставляем только Москву; пустые регионы заменяем на "", чтобы strip не упал
    moscow = df[df["region"].fillna("").str.strip() == "Москва"].copy()

    # Переводим datetime в дату без времени; битые значения становятся NaT
    moscow["date"] = pd.to_datetime(moscow["datetime"], errors="coerce").dt.normalize()

    # Убираем записи без корректной даты и дубликаты по id
    moscow = moscow.dropna(subset=["date"]).drop_duplicates(subset="id")

    # Считаем число ДТП за каждый день, в индексе дата, значение accidents
    counts = moscow.groupby("date").size().rename("accidents")

    # Строим непрерывный календарь от первого до последнего дня с ДТП
    # и заполняем дни без записей нулями
    full = pd.date_range(counts.index.min(), counts.index.max(), freq="D")
    daily = counts.reindex(full, fill_value=0).to_frame()
    daily.index.name = "date"

    # Признаки: лаги и скользящее среднее считаем только по прошлым дням
    daily["lag_1"] = daily["accidents"].shift(1)
    daily["lag_7"] = daily["accidents"].shift(7)
    daily["roll_7"] = daily["accidents"].shift(1).rolling(7).mean()

    # Календарные признаки: день недели (0 = понедельник) и месяц
    daily["dow"] = daily.index.day_of_week
    daily["month"] = daily.index.month

    # Удаляем первые 7 дней, где лаги ещё не определены
    daily = daily.dropna(subset=["lag_1", "lag_7", "roll_7"])

    # Приводим строки к типам, которые понимает драйвер БД (без numpy)
    out = [
        (
            row.date.date(),
            int(row.accidents),
            float(row.lag_1),
            float(row.lag_7),
            float(row.roll_7),
            int(row.dow),
            int(row.month),
        )
        for row in daily.reset_index().itertuples(index=False)
    ]

    # Вставляем строки; дни, которые уже есть в таблице, пропускаются по ключу date
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO daily
                (date, accidents, lag_1, lag_7, roll_7, dow, month)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING
            """,
            out,
        )
    conn.commit()