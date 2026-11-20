import math
from dataclasses import asdict

from db.connection import get_connection
from entity.model_record import ModelRecord


def fetch_model(model_id: int, page: int, page_size: int):
    base_sql = (
        f"SELECT "
        f"  m.name, \n"
        f"  r.id, \n"
        f"  r.params, \n"
        f"  r.feature_version, \n"
        f"  r.random_seed, \n"
        f"  r.artifact_path, \n"
        f"  r.train_start, \n"
        f"  r.train_end, \n"
        f"  r.test_start, \n"
        f"  r.test_end, \n"
        f"  r.n_train, \n"
        f"  r.n_test, \n"
        f"  r.mae_train, \n"
        f"  r.mae_test, \n"
        f"  r.mase_train, \n"
        f"  r.mase_test \n"
        f"FROM  runs r \n"
        f"JOIN models m ON r.model_id = m.id AND r.model_id = {model_id} \n"
        f"ORDER BY r.id DESC"
    )

    with get_connection() as conn:
        total = conn.execute(f"SELECT COUNT(*) FROM runs WHERE model_id = {model_id}").fetchone()[0]

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
        "items": [asdict(ModelRecord(*row)) for row in rows],
        "total": total,
        "page": page,
        "pages": pages,
    }