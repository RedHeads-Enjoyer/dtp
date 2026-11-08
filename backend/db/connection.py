# db/connection.py
import os
import psycopg

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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_dtp (
                id INTEGER PRIMARY KEY,
                tags TEXT,
                category TEXT,
                region TEXT,
                county TEXT,
                address TEXT,
                longitude DOUBLE PRECISION,
                latitude DOUBLE PRECISION,
                nearby TEXT,
                datetime TIMESTAMP,
                light TEXT,
                weather TEXT,
                road_conditions TEXT,
                participants_count INTEGER,
                participant_categories TEXT,
                severity TEXT,
                dead_count INTEGER,
                injured_count INTEGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS dtp_load_log (
                id            SERIAL PRIMARY KEY,
                file_name     TEXT,
                started_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
                finished_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
                status        TEXT NOT NULL,
                rows_total    INTEGER,
                rows_inserted INTEGER,
                error         TEXT
            )
        """)