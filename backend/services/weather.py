import time

import requests

from db.connection import get_connection
from entity.raw_weather_record import RawWeatherRecord
from entity.weather_record import WeatherRecord
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
            "INSERT INTO raw_weather (url) VALUES (%s) ON CONFLICT (url) DO NOTHING",
            rows,
        )
    conn.commit()
    return len(rows)


def _download(url: str) -> str:
    resp = requests.get(url, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text.replace("\x00", "")


def _pending(conn) -> list[tuple[int, str]]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, url FROM raw_weather "
            "WHERE html IS NULL AND fetch_error IS NULL ORDER BY id"
        )
        return cur.fetchall()

def _set_fetch_error(conn, row_id: int, exc: Exception) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE raw_weather SET fetch_error = %s, responded_at = now() WHERE id = %s",
            (f"{type(exc).__name__}: {exc}"[:1000], row_id),
        )
    conn.commit()

def _fetch_one(conn, row_id: int, url: str) -> str | None:
    try:
        html = _download(url)
    except Exception as exc:
        _set_fetch_error(conn, row_id, exc)
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE raw_weather SET html = %s, fetch_error = NULL, responded_at = now() WHERE id = %s",
                (html, row_id),
            )
        conn.commit()
        return html
    except Exception as exc:
        conn.rollback()
        _set_fetch_error(conn, row_id, exc)
        return None



def fill_pending(pause: float = 3.0) -> None:
    with get_connection() as conn:
        if not try_lock(LOCK_KEY, conn):
            return
        try:
            for row_id, url in _pending(conn):
                html = _fetch_one(conn, row_id, url)
                if html is not None:
                    parse_one(row_id, url, html)
                time.sleep(pause)
        finally:
            unlock(LOCK_KEY, conn)


def get_raw_weather(page: int = 1) -> dict:
    return fetch_page(RawWeatherRecord, "raw_weather", "id DESC, id", page, 500)

def get_weather(page: int = 1) -> dict:
    return fetch_page(WeatherRecord, "weather", "observed_date DESC, id", page, 500)