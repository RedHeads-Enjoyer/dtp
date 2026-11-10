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

DAILY_DDL = """
    CREATE TABLE IF NOT EXISTS daily (
        id          SERIAL PRIMARY KEY,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
        date        DATE UNIQUE,
        accidents   INTEGER NOT NULL CHECK (accidents >= 0),
        lag_1       DOUBLE PRECISION NOT NULL,
        lag_7       DOUBLE PRECISION NOT NULL,
        roll_7      DOUBLE PRECISION NOT NULL,
        dow         SMALLINT NOT NULL CHECK (dow BETWEEN 0 AND 6),
        month       SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12)
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
        id           SERIAL PRIMARY KEY,
        url          TEXT UNIQUE,
        requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        responded_at TIMESTAMPTZ,
        html         TEXT,
        fetch_error  TEXT,
        parse_error  TEXT
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

FEATURES_DDL = """
    CREATE TABLE IF NOT EXISTS features (
        version        INTEGER NOT NULL,
        date           DATE NOT NULL,
        accidents      INTEGER,
        lag_1          DOUBLE PRECISION,
        lag_7          DOUBLE PRECISION,
        roll_7         DOUBLE PRECISION,
        dow            SMALLINT,
        month          SMALLINT,
        temp_dev       NUMERIC(4,1),
        temp_min       NUMERIC(4,1),
        temp_max       NUMERIC(4,1),
        temp_mean      NUMERIC(4,1),
        precipitation  NUMERIC(6,1),
        PRIMARY KEY (date, version)
    )
"""

MODELS_DDL = """
    CREATE TABLE IF NOT EXISTS models (
        id          SERIAL PRIMARY KEY,
        name        TEXT NOT NULL UNIQUE,
        created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
"""

RUNS_DDL = """
    CREATE TABLE IF NOT EXISTS runs (
        id               SERIAL PRIMARY KEY,
        model_id         INTEGER NOT NULL REFERENCES models(id),
        params           JSONB NOT NULL DEFAULT '{}'::jsonb,
        feature_version  INTEGER NOT NULL,
        random_state     INTEGER,
        artifact_path    TEXT,
        train_start  DATE,
        train_end    DATE,
        val_start    DATE,
        val_end      DATE,
        test_start   DATE,
        test_end     DATE,
        n_train      INTEGER,
        n_val        INTEGER,
        n_test       INTEGER,
        mae_train    DOUBLE PRECISION,
        mae_val      DOUBLE PRECISION,
        mae_test     DOUBLE PRECISION,
        mase_train   DOUBLE PRECISION,
        mase_val     DOUBLE PRECISION,
        mase_test    DOUBLE PRECISION
    )
"""