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
        created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
        date                  DATE PRIMARY KEY,
        accidents_lag_1       NUMERIC(6,2) NOT NULL,
        accidents_lag_7       NUMERIC(6,2) NOT NULL,
        accidents_roll_7      NUMERIC(6,2) NOT NULL,
        dow                   SMALLINT NOT NULL CHECK (dow BETWEEN 0 AND 6),
        month                 SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12)
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

WEATHER_RAW_DDL = """
    CREATE TABLE IF NOT EXISTS weather_raw (
        url          TEXT PRIMARY KEY,
        requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        responded_at TIMESTAMPTZ,
        html         TEXT,
        fetch_error  TEXT,
        parse_error  TEXT
    )
"""

WEATHER_PARSED_DDL = """
    CREATE TABLE IF NOT EXISTS weather_parsed (
        station_id      INTEGER NOT NULL,
        observed_date   DATE NOT NULL,
        temp_min        NUMERIC(6,1),
        temp_mean       NUMERIC(6,1),
        temp_max        NUMERIC(6,1),
        temp_dev        NUMERIC(6,1),
        precipitation   NUMERIC(6,1),
        parsed_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
        PRIMARY KEY (station_id, observed_date)
    )
"""

WEATHER_DDL = """
    CREATE TABLE IF NOT EXISTS weather (       
        station_id            INTEGER NOT NULL,
        observed_date         DATE NOT NULL,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
        temp_mean_lag_1       NUMERIC(6,2),
        temp_mean_mean_3      NUMERIC(6,2),
        temp_mean_mean_7      NUMERIC(6,2),
        temp_min_lag_1        NUMERIC(6,2),
        temp_min_min_3        NUMERIC(6,2),
        temp_max_lag_1        NUMERIC(6,2),
        temp_change           NUMERIC(6,2),
        temp_dev_lag_1        NUMERIC(6,2),
        precipitation_lag_1   NUMERIC(6,2),
        precipitation_sum_3   NUMERIC(6,2),
        precipitation_sum_7   NUMERIC(6,2),
        UNIQUE (station_id, observed_date)
    )     
"""

FEATURES_DDL = """
    CREATE TABLE IF NOT EXISTS features (
        version               INTEGER NOT NULL,
        date                  DATE,
        accidents_lag_1       NUMERIC(6,2) NOT NULL,
        accidents_lag_7       NUMERIC(6,2) NOT NULL,
        accidents_roll_7      NUMERIC(6,2) NOT NULL,
        dow                   SMALLINT NOT NULL CHECK (dow BETWEEN 0 AND 6),
        month                 SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
        temp_mean_lag_1       NUMERIC(6,2),
        temp_mean_mean_3      NUMERIC(6,2),
        temp_mean_mean_7      NUMERIC(6,2),
        temp_min_lag_1        NUMERIC(6,2),
        temp_min_min_3        NUMERIC(6,2),
        temp_max_lag_1        NUMERIC(6,2),
        temp_change           NUMERIC(6,2),
        temp_dev_lag_1        NUMERIC(6,2),
        precipitation_lag_1   NUMERIC(6,2),
        precipitation_sum_3   NUMERIC(6,2),
        precipitation_sum_7   NUMERIC(6,2),
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