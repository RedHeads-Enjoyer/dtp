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

RAW_WEATHER_DDL = """
    CREATE TABLE IF NOT EXISTS raw_weather (
        id      SERIAL PRIMARY KEY,
        url     TEXT UNIQUE,
        requested_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
        responded_at  TIMESTAMPTZ,
        html    TEXT,
        error   TEXT
    )
"""

WEATHER_DDL = """
    CREATE TABLE IF NOT EXISTS weather (
        id              SERIAL PRIMARY KEY,
        station_id      INTEGER NOT NULL,
        observed_date   DATE NOT NULL,
        temp_min        NUMERIC(4,1),
        temp_mean       NUMERIC(4,1),
        temp_max        NUMERIC(4,1),
        temp_dev        NUMERIC(4,1),
        precipitation   NUMERIC(6,1),
        raw_id          INTEGER REFERENCES raw_weather(id),
        parsed_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
        UNIQUE (station_id, observed_date)
    )
"""