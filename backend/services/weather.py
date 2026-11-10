import time

import requests
import pandas as pd

from db.connection import get_connection
from entity.weather_parsed_record import WeatherParsedRecord
from entity.weather_raw_record import WeatherRawRecord
from entity.weather_record import WeatherRecord
from services.feature import update_features
from services.parser import parse_one
from services.utils import fetch_page, try_lock, unlock

BASE_URL = "https://www.pogodaiklimat.ru/monitor.php"
LOCK_KEY = 676767
HTTP_TIMEOUT = 15


def weather_url(station_id: int, year: int, month: int) -> str:
    return f"{BASE_URL}?id={station_id}&month={month}&year={year}"


def enqueue_months(conn, station_id: int, months: set[tuple[int, int]]) -> int:
    rows = [(weather_url(station_id, y, m),) for y, m in sorted(months)]
    if not rows:
        return 0
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO weather_raw (url) VALUES (%s) ON CONFLICT (url) DO NOTHING",
            rows,
        )
    conn.commit()
    return len(rows)


def _download(url: str) -> str:
    resp = requests.get(url, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text.replace("\x00", "")


def _pending(conn) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT url FROM weather_raw "
            "WHERE html IS NULL AND fetch_error IS NULL ORDER BY url"
        )
        return [row[0] for row in cur.fetchall()]

def _set_fetch_error(conn, url: str, exc: Exception) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE weather_raw SET fetch_error = %s, responded_at = now() WHERE url = %s",
            (f"{type(exc).__name__}: {exc}"[:1000], url),
        )
    conn.commit()

def _update_weather(conn) -> None:
    print("_update_weather")
    # Читаем все наблюдения погоды и превращаем их в DataFrame
    result = get_weather_parsed(1, -1)
    df = pd.DataFrame(result["items"])

    print("df")
    print(df)

    if df.empty:
        print("df.empty")
        return

    # Переводим дату в datetime и убираем дубликаты по станции и дню
    df["observed_date"] = pd.to_datetime(df["observed_date"])
    df = df.drop_duplicates(subset=["station_id", "observed_date"])

    out = []
    # Считаем признаки отдельно для каждой станции
    for station_id, g in df.groupby("station_id"):
        g = g.set_index("observed_date").sort_index()

        # Дни, по которым реально есть наблюдения; в них будем писать строки
        observed_days = g.index

        # Непрерывный календарь без пропусков, чтобы shift считал дни, а не строки
        full = pd.date_range(g.index.min(), g.index.max(), freq="D")
        g = g.reindex(full)

        # Признаки: только по прошлым дням (shift(1) перед окном), иначе утечка
        f = pd.DataFrame(index=full)
        f["temp_mean_lag_1"] = g["temp_mean"].shift(1)
        f["temp_mean_mean_3"] = g["temp_mean"].shift(1).rolling(3).mean()
        f["temp_mean_mean_7"] = g["temp_mean"].shift(1).rolling(7).mean()
        f["temp_min_lag_1"] = g["temp_min"].shift(1)
        f["temp_min_min_3"] = g["temp_min"].shift(1).rolling(3).min()
        f["temp_max_lag_1"] = g["temp_max"].shift(1)
        f["temp_change"] = g["temp_mean"].shift(1) - g["temp_mean"].shift(2)
        f["temp_dev_lag_1"] = g["temp_dev"].shift(1)
        f["precipitation_lag_1"] = g["precipitation"].shift(1)
        f["precipitation_sum_3"] = g["precipitation"].shift(1).rolling(3).sum()
        f["precipitation_sum_7"] = g["precipitation"].shift(1).rolling(7).sum()

        # Оставляем только дни с наблюдениями; строки с NaN не выкидываем,
        # потому что погодные признаки могут быть пустыми и в БД это допустимо
        f = f.loc[observed_days]

        for day, row in f.iterrows():
            out.append((
                int(station_id),
                day.date(),
                *[None if pd.isna(v) else float(v) for v in row.values],
            ))

    if not out:
        return

    # Пересчёт полный, поэтому очищаем и пишем в одной транзакции
    with conn.cursor() as cur:
        cur.execute("DELETE FROM weather")
        cur.executemany(
            """
            INSERT INTO weather
                (station_id, observed_date,
                 temp_mean_lag_1, temp_mean_mean_3, temp_mean_mean_7,
                 temp_min_lag_1, temp_min_min_3, temp_max_lag_1,
                 temp_change, temp_dev_lag_1,
                 precipitation_lag_1, precipitation_sum_3, precipitation_sum_7)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            out,
        )
    conn.commit()
def _fetch_one(conn, url: str) -> str | None:
    try:
        html = _download(url)
    except Exception as exc:
        _set_fetch_error(conn, url, exc)
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE weather_raw SET html = %s, fetch_error = NULL, responded_at = now() "
                "WHERE url = %s",
                (html, url),
            )
        conn.commit()
        return html
    except Exception as exc:
        conn.rollback()
        _set_fetch_error(conn, url, exc)
        return None



def fill_pending(pause: float = 3.0) -> None:
    with get_connection() as conn:
        if not try_lock(LOCK_KEY, conn):
            return
        try:
            for url in _pending(conn):
                html = _fetch_one(conn, url)
                if html is not None:
                    parse_one(url, html)
                time.sleep(pause)
        finally:
            unlock(LOCK_KEY, conn)

        print("fill_pending")
        if weather_parsing_is_complete(conn):
            print("weather_parsing_is_complete")
            _update_weather(conn)
            update_features(conn)

def weather_parsing_is_complete(conn) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM weather_raw "
            "WHERE html IS NULL AND fetch_error IS NULL"
        )
        return cur.fetchone()[0] == 0

def get_weather_raw(page: int = 1) -> dict:
    return fetch_page(WeatherRawRecord, "weather_raw", "url DESC", page, 500)

def get_weather_parsed(page: int = 1, page_size = 500) -> dict:
    return fetch_page(WeatherParsedRecord, "weather_parsed", "observed_date DESC, station_id", page, page_size)

def get_weather(page: int = 1, page_size = 500) -> dict:
    return fetch_page(WeatherRecord, "weather", "station_id DESC, station_id", page, page_size)