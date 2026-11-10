import os
import psycopg

from db.tables import RAW_DTP_DDL, LOAD_LOG_DDL, WEATHER_RAW_DDL, WEATHER_PARSED_DDL, DAILY_DDL, FEATURES_DDL, \
    MODELS_DDL, \
    RUNS_DDL, WEATHER_DDL
from db.values import MODELS_INSERT


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
            # Создание моделей
            conn.execute(RAW_DTP_DDL)
            conn.execute(DAILY_DDL)
            conn.execute(LOAD_LOG_DDL)
            conn.execute(WEATHER_RAW_DDL)
            conn.execute(WEATHER_PARSED_DDL)
            conn.execute(WEATHER_DDL)
            conn.execute(FEATURES_DDL)
            conn.execute(MODELS_DDL)
            conn.execute(RUNS_DDL)

            # Заполнение
            conn.execute(MODELS_INSERT)