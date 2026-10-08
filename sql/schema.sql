-- Star schema: one fact table, three dimensions.
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_area;
DROP TABLE IF EXISTS dim_property;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_area (
    area_id    INTEGER PRIMARY KEY,
    area_name  TEXT NOT NULL
);

CREATE TABLE dim_property (
    property_id        INTEGER PRIMARY KEY,
    property_type      TEXT,
    property_sub_type  TEXT,
    reg_type           TEXT
);

CREATE TABLE dim_date (
    date_id   INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year      INTEGER NOT NULL,
    quarter   INTEGER NOT NULL,
    month     INTEGER NOT NULL
);

CREATE TABLE fact_transactions (
    transaction_id  TEXT PRIMARY KEY,
    date_id         INTEGER NOT NULL REFERENCES dim_date(date_id),
    area_id         INTEGER NOT NULL REFERENCES dim_area(area_id),
    property_id     INTEGER NOT NULL REFERENCES dim_property(property_id),
    project_name    TEXT,
    rooms           TEXT,
    value_aed       NUMERIC NOT NULL,
    area_sqm        NUMERIC NOT NULL,
    price_per_sqm   NUMERIC NOT NULL,
    is_bulk         BOOLEAN NOT NULL
);

CREATE INDEX idx_fact_date ON fact_transactions(date_id);
CREATE INDEX idx_fact_area ON fact_transactions(area_id);
CREATE INDEX idx_fact_property ON fact_transactions(property_id);
