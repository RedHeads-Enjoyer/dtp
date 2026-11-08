import csv
import io
from db.connection import get_connection

COLUMNS = [
    "id", "tags", "category", "region", "county", "address",
    "longitude", "latitude", "nearby", "datetime", "light",
    "weather", "road_conditions", "participants_count",
    "participant_categories", "severity", "dead_count", "injured_count",
]


def import_dtp(content: bytes) -> int:
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))

    rows = [
        {k: (v or None) for k, v in row.items()}
        for row in reader
    ]

    if not rows:
        return 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO dtp VALUES (
                    %(id)s, %(tags)s, %(category)s, %(region)s, %(county)s,
                    %(address)s, %(longitude)s, %(latitude)s, %(nearby)s,
                    %(datetime)s, %(light)s, %(weather)s, %(road_conditions)s,
                    %(participants_count)s, %(participant_categories)s,
                    %(severity)s, %(dead_count)s, %(injured_count)s
                )
                ON CONFLICT (id) DO NOTHING
                """,
                rows,
            )
    return len(rows)

def get_dtp(page) -> dict:
    page = max(page, 1)
    page_size = 500
    offset = (page - 1) * page_size

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM dtp")
            total = cur.fetchone()[0]

            cur.execute(
                f"""
                SELECT {", ".join(COLUMNS)}
                FROM dtp
                ORDER BY datetime DESC, id
                LIMIT %s OFFSET %s
                """,
                (page_size, offset),
            )
            rows = cur.fetchall()

    items = [
        dict(zip(COLUMNS, row))
        for row in rows
    ]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
    }