RAW_DTP_DDL = """
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
"""

LOAD_LOG_DDL = """
    CREATE TABLE IF NOT EXISTS dtp_load_log (
        id            SERIAL PRIMARY KEY,
        file_name     TEXT,
        started_at    TIMESTAMPTZ NOT NULL,
        finished_at   TIMESTAMPTZ,
        status        TEXT NOT NULL,
        rows_total    INTEGER,
        rows_inserted INTEGER,
        error         TEXT
    )
"""