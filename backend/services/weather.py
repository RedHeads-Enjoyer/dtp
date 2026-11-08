import time

import requests

from db.connection import get_connection
from entity.raw_weather_record import RawWeatherRecord
from services.utils import fetch_page

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


def _try_lock(conn) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
        return cur.fetchone()[0]


def _unlock(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
    conn.commit()


def _pending(conn) -> list[tuple[int, str]]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, url FROM raw_weather "
            "WHERE html IS NULL AND error IS NULL ORDER BY id"
        )
        return cur.fetchall()


def _fetch_one(conn, row_id: int, url: str) -> None:
    try:
        html = _download(url)
        sql = "UPDATE raw_weather SET html = %s, error = NULL, responded_at = now() WHERE id = %s"
        params = (html, row_id)
    except requests.RequestException as exc:
        sql = "UPDATE raw_weather SET error = %s, responded_at = now() WHERE id = %s"
        params = (f"{type(exc).__name__}: {exc}"[:1000], row_id)

    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    except Exception as exc:
        conn.rollback()
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE raw_weather SET error = %s, responded_at = now() WHERE id = %s",
                (f"{type(exc).__name__}: {exc}"[:1000], row_id),
            )
        conn.commit()


def fill_pending(pause: float = 10.0) -> None:
    with get_connection() as conn:
        if not _try_lock(conn):
            return
        try:
            for row_id, url in _pending(conn):
                print(row_id, url)
                _fetch_one(conn, row_id, url)
                time.sleep(pause)
        finally:
            _unlock(conn)


def get_weather(page: int = 1) -> dict:
    return fetch_page(RawWeatherRecord, "raw_weather", "id DESC, id", page, -1)