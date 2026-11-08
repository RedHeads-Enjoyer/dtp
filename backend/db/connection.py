import os
import psycopg

from db.tables import RAW_DTP_DDL, LOAD_LOG_DDL, RAW_WEATHER_DDL, WEATHER_DDL


def get_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )

def init_db():
    with get_connection() as conn:
        with get_connection() as conn:
            conn.execute(RAW_DTP_DDL)
            conn.execute(LOAD_LOG_DDL)
            conn.execute(RAW_WEATHER_DDL)
            conn.execute(WEATHER_DDL)