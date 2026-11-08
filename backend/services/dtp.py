import csv
import io
import math
from dataclasses import asdict, fields
from datetime import datetime, timezone
from typing import Optional, Type, TypeVar

from db.connection import get_connection
from entity.dtp_record import DTP_COLUMNS, DtpRecord
from entity.load_log_record import LoadLogRecord

T = TypeVar("T")

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


def import_dtp(content: bytes, file_name: str) -> int:
    started_at = datetime.now(timezone.utc)

    try:
        text = content.decode("utf-8-sig")
        records = [
            DtpRecord.from_csv_row(row)
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
        return inserted

    except Exception as e:
        _write_log(file_name, started_at, "error", error=str(e)[:1000])
        raise


def _fetch_page(cls: Type[T], table: str, order_by: str, page: int, page_size: int) -> dict:
    page = max(page, 1)
    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)
    columns = [f.name for f in fields(cls)]

    with get_connection() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        rows = conn.execute(
            f"SELECT {', '.join(columns)} FROM {table} "
            f"ORDER BY {order_by} "
            "LIMIT %s OFFSET %s",
            (page_size, (page - 1) * page_size),
        ).fetchall()

    return {
        "items": [asdict(cls(*row)) for row in rows],
        "total": total,
        "page": page,
        "pages": math.ceil(total / page_size),
    }


def get_dtp(page: int = 1, page_size: int = MAX_PAGE_SIZE) -> dict:
    return _fetch_page(
        DtpRecord, "raw_dtp", "datetime DESC, id", page, page_size
    )


def get_load_log(page: int = 1, page_size: int = MAX_PAGE_SIZE) -> dict:
    return _fetch_page(
        LoadLogRecord, "dtp_load_log", "started_at DESC, id DESC", page, page_size
    )