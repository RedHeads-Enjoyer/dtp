import time

import requests

from db.connection import get_connection
from entity.weather_record import WeatherRecord
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
            "INSERT INTO raw_weather (url, html) VALUES (%s, NULL) "
            "ON CONFLICT (url) DO NOTHING",
            rows,
        )
    conn.commit()
    return len(rows)


def _download(url: str) -> str:
    resp = requests.get(url, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text.replace("\x00", "")


def _save_error(conn, row_id: int, message: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE raw_weather SET error = %s, responded_at = now() WHERE id = %s",
            (message[:1000], row_id),
        )
    conn.commit()


def fill_pending(pause: float = 10.0) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
            if not cur.fetchone()[0]:
                return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, url FROM raw_weather "
                    "WHERE html IS NULL AND error IS NULL "
                    "ORDER BY id"
                )
                pending = cur.fetchall()

            for row_id, url in pending:

                print(row_id, url)

                try:
                    html = _download(url)
                except requests.RequestException as exc:
                    _save_error(conn, row_id, str(exc))
                    time.sleep(pause)
                    continue

                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE raw_weather "
                            "SET html = %s, error = NULL, responded_at = now() "
                            "WHERE id = %s",
                            (html, row_id),
                        )
                    conn.commit()
                except Exception as exc:
                    conn.rollback()
                    _save_error(conn, row_id, f"{type(exc).__name__}: {exc}")

                time.sleep(pause)
        finally:
            with conn.cursor() as cur:
                cur.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
            conn.commit()


def get_weather(page: int = 1) -> dict:
    return fetch_page(WeatherRecord, "raw_weather", "id DESC, id", page, -1)