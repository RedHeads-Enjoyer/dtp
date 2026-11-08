import calendar
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from db.connection import get_connection


def _num(text: str) -> Decimal | None:
    text = text.replace(",", ".").replace("+", "").strip()
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def parse_table(html: str) -> list[list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    wrap = soup.find("div", class_="climate-table-wrap")
    if wrap is None:
        raise ValueError("не найден блок climate-table-wrap")
    table = wrap.find("table")
    if table is None:
        raise ValueError("в climate-table-wrap нет таблицы")
    return [
        [td.get_text(strip=True) for td in tr.find_all("td")]
        for tr in table.find_all("tr")
    ]


def _save_month(conn, raw_id: int, station_id: int, year: int, month: int, html: str) -> int:
    rows = [r for r in parse_table(html) if len(r) >= 6 and r[0].isdigit()]
    if not rows:
        raise ValueError(f"в странице raw_id={raw_id} нет строк с днями")

    days_in_month = calendar.monthrange(year, month)[1]
    rows = [r for r in rows if 1 <= int(r[0]) <= days_in_month]

    with conn.cursor() as cur:
        for r in rows:
            observed = date(year, month, int(r[0]))
            cur.execute(
                """
                INSERT INTO weather
                    (station_id, observed_date, temp_min, temp_mean, temp_max,
                     temp_dev, precipitation, raw_id, parsed_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (station_id, observed_date) DO UPDATE SET
                    temp_min = EXCLUDED.temp_min,
                    temp_mean = EXCLUDED.temp_mean,
                    temp_max = EXCLUDED.temp_max,
                    temp_dev = EXCLUDED.temp_dev,
                    precipitation = EXCLUDED.precipitation,
                    raw_id = EXCLUDED.raw_id,
                    parsed_at = now()
                """,
                (
                    station_id, observed,
                    _num(r[1]), _num(r[2]), _num(r[3]), _num(r[4]), _num(r[5]),
                    raw_id,
                ),
            )
    return len(rows)

def _parse_url(url: str) -> tuple[int, int, int]:
    q = parse_qs(urlparse(url).query)
    return int(q["id"][0]), int(q["year"][0]), int(q["month"][0])

def parse_one(raw_id: int, url: str, html: str) -> int:
    with get_connection() as conn:
        try:
            station_id, year, month = _parse_url(url)
            total = _save_month(conn, raw_id, station_id, year, month, html)
            conn.commit()
            return total
        except Exception as exc:
            conn.rollback()
            _set_parse_error(conn, raw_id, exc)
            return 0

def _set_parse_error(conn, raw_id: int, exc: Exception) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE raw_weather SET parse_error = %s WHERE id = %s",
                (f"{type(exc).__name__}: {exc}"[:1000], raw_id),
            )
        conn.commit()
    except Exception as inner:
        conn.rollback()
        print(f"не удалось записать parse_error raw_id={raw_id}: {inner}")