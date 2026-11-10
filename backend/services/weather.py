import time

import requests

from db.connection import get_connection
from entity.weather_parsed_record import WeatherParsedRecord
from entity.weather_raw_record import WeatherRawRecord
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

        if weather_is_complete(conn):
            update_features(conn)

def weather_is_complete(conn) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM weather_raw "
            "WHERE html IS NULL AND fetch_error IS NULL"
        )
        return cur.fetchone()[0] == 0

def get_weather_raw(page: int = 1) -> dict:
    return fetch_page(WeatherRawRecord, "weather_raw", "requested_at DESC, url", page, 500)

def get_weather_parsed(page: int = 1) -> dict:
    return fetch_page(WeatherParsedRecord, "weather_parsed", "observed_date DESC, station_id", page, 500)