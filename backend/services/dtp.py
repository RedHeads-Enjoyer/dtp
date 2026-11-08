import csv
import io
import math
import datetime as dt

from dataclasses import asdict

from db.connection import get_connection
from entity.DtpLoadLogRecord import DTP_LOAD_LOG_COLUMNS, DtpLoadLogRecord
from entity.DtpRecord import DtpRecord, DTP_COLUMNS

def _write_log(file_name, started_at, status, rows_total=0, rows_inserted=0, error=None):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dtp_load_log
                (file_name, started_at, status,
                 rows_total, rows_inserted, error)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (file_name, started_at, status, rows_total, rows_inserted, error),
        )

def import_dtp(content: bytes, file_name: str = "") -> int:
    started_at = dt.datetime.now(dt.timezone.utc)

    try:
        reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
        records = [DtpRecord.from_csv_row(row) for row in reader]

        if not records:
            _write_log(file_name, started_at, "empty")
            return 0

        insert_sql = (
            f"INSERT INTO raw_dtp ({', '.join(DTP_COLUMNS)}) "
            f"VALUES ({', '.join(f'%({c})s' for c in DTP_COLUMNS)}) "
            "ON CONFLICT (id) DO NOTHING"
        )

        params = [r.to_params() for r in records]

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(insert_sql, params)
                inserted = cur.rowcount

        _write_log(file_name, started_at, "ok", rows_total=len(records), rows_inserted=inserted)
        return inserted

    except Exception as e:
        _write_log(file_name, started_at, "error", error=str(e)[:1000])
        raise


def get_dtp(page: int, page_size = 500) -> dict:
    page = max(page, 1)

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM raw_dtp")
        total = cur.fetchone()[0]

        cur.execute(
            f"SELECT {', '.join(DTP_COLUMNS)} FROM raw_dtp "
            "ORDER BY datetime DESC, id "
            "LIMIT %s OFFSET %s",
            (page_size, (page - 1) * page_size),
        )
        items = [
            asdict(DtpRecord(**dict(zip(DTP_COLUMNS, row))))
            for row in cur.fetchall()
        ]

    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": math.ceil(total / page_size),
    }

def get_load_log() -> dict:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM dtp_load_log")
        total = cur.fetchone()[0]

        cur.execute(
            f"SELECT {', '.join(DTP_LOAD_LOG_COLUMNS)} FROM dtp_load_log "
            "ORDER BY started_at DESC, id DESC "
        )
        items = [
            asdict(DtpLoadLogRecord(**dict(zip(DTP_LOAD_LOG_COLUMNS, row))))
            for row in cur.fetchall()
        ]

    return {
        "items": items,
        "total": total,
    }