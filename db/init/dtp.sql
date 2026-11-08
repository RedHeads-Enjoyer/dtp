CREATE TABLE IF NOT EXISTS dtp (
    id                     TEXT PRIMARY KEY,
    tags                   TEXT,
    category               TEXT,
    region                 TEXT,
    county                 TEXT,
    address                TEXT,
    longitude              DOUBLE PRECISION,
    latitude               DOUBLE PRECISION,
    nearby                 TEXT,
    datetime               TIMESTAMP NOT NULL,
    light                  TEXT,
    weather                TEXT,
    road_conditions        TEXT,
    participants_count     INTEGER,
    participant_categories TEXT,
    severity               TEXT,
    dead_count             INTEGER,
    injured_count          INTEGER,
    loaded_at              TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_dtp_datetime ON dtp (datetime);