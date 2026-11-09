import math
from dataclasses import fields, asdict
from typing import Type, TypeVar

from db.connection import get_connection


T = TypeVar("T")

def fetch_page(cls: Type[T], table: str, order_by: str, page: int, page_size: int) -> dict:
    columns = [f.name for f in fields(cls)]
    base_sql = (
        f"SELECT {', '.join(columns)} FROM {table} "
        f"ORDER BY {order_by}"
    )

    with get_connection() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

        if page_size == -1:
            rows = conn.execute(base_sql).fetchall()
            page = 1
            pages = 1
        else:
            page = max(page, 1)
            page_size = max(page_size, 1)
            rows = conn.execute(
                base_sql + " LIMIT %s OFFSET %s",
                (page_size, (page - 1) * page_size),
            ).fetchall()
            pages = math.ceil(total / page_size)

    return {
        "items": [asdict(cls(*row)) for row in rows],
        "total": total,
        "page": page,
        "pages": pages,
    }


def try_lock(lock_key: int, conn) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT pg_try_advisory_lock(%s)", (lock_key,))
        return cur.fetchone()[0]


def unlock(lock_key: int, conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT pg_advisory_unlock(%s)", (lock_key,))
    conn.commit()