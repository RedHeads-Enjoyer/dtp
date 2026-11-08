import csv
import io
from datetime import datetime, timezone
from typing import Optional

from db.connection import get_connection
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
            SELECT DISTINCT EXTRACT(YEAR FROM datetime)::int,
                            EXTRACT(MONTH FROM datetime)::int
            FROM raw_dtp
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

        return inserted

    except Exception as e:
        _write_log(file_name, started_at, "error", error=str(e)[:1000])
        raise


def get_dtp(page: int = 1) -> dict:
    return fetch_page(RawDtpRecord, "raw_dtp", "datetime DESC, id", page, 500)


def get_load_log(page: int = 1) -> dict:
    return fetch_page(LoadLogRecord, "dtp_load_log", "started_at DESC, id DESC", page, 500)