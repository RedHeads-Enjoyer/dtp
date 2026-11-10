from entity.feature_record import FeatureRecord
from services.utils import fetch_page


def _get_next_version(conn) -> int | None:
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(version), 0) FROM features")
        return cur.fetchone()[0] + 1


def _features_to_insert(conn):
    with conn.cursor() as cur:
        cur.execute("""
            WITH f AS (
                SELECT date
                FROM features
            )
            SELECT d.date
            FROM daily d
            LEFT JOIN f ON f.date = d.date
            WHERE f.date ISNULL
            """)
        return [row[0] for row in cur.fetchall()]

def _update(dates, version, conn):

    sql = """
        INSERT INTO features
            (version, date, accidents_lag_1, accidents_lag_7, accidents_roll_7, dow, month, 
             temp_mean_lag_1, temp_mean_mean_3, temp_mean_mean_7, temp_min_lag_1, temp_min_min_3, temp_max_lag_1, 
             temp_change, temp_dev_lag_1, precipitation_lag_1, precipitation_sum_3, precipitation_sum_7)
        SELECT
            %(version)s,
            d.date,
            d.accidents_lag_1,
            d.accidents_lag_7,
            d.accidents_roll_7,
            d.dow,
            d.month,
            w.temp_mean_lag_1,
            w.temp_mean_mean_3,
            w.temp_mean_mean_7,
            w.temp_min_lag_1,
            w.temp_min_min_3,
            w.temp_max_lag_1,
            w.temp_change,
            w.temp_dev_lag_1,
            w.precipitation_lag_1,
            w.precipitation_sum_3,
            w.precipitation_sum_7
        FROM daily d
        JOIN weather w ON w.observed_date = d.date
        WHERE d.date = ANY(%(dates)s)
    """

    with conn.cursor() as cur:
        cur.execute(sql, {
        "version": version,
        "dates": dates,
    })

def update_features(conn):
    try:
        dates = _features_to_insert(conn)
        if not dates:
            return None
        version = _get_next_version(conn)
        _update(dates, version, conn)
        conn.commit()
        return version
    except Exception:
        conn.rollback()
        raise

def get_features(page: int = 1, page_size: int = 500) -> dict:
    return fetch_page(FeatureRecord, "features", "date DESC", page, page_size)

def is_features_ready(conn) -> bool:
    return len(_features_to_insert(conn)) == 0


