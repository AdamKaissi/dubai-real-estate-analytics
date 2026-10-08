# Dubai Real Estate Market Analytics

End-to-end analysis of registered Dubai Land Department (DLD) sales transactions: data cleaning in Python,
a PostgreSQL star schema, SQL analysis with window functions, a regression on price drivers, and a Power BI dashboard.

> Status: scaffold. Replace each section marked TODO with your real findings once you have run the pipeline on the real data.

## Question
TODO: One or two sentences. Example format: "How have prices per square metre moved across Dubai's most active
communities since 2019, and how much of the variation is explained by area, property type, and off-plan status?"

## Data
- Source: Dubai Land Department open data, via Dubai Pulse (registered sales transactions).
- Coverage: TODO (date range and row count after cleaning, from `docs/cleaning_log.csv`).
- Raw data is not committed to this repo. See "Reproduce" below.

## Method
1. `src/01_inspect.py` checks the file and column mapping.
2. `src/02_clean.py` cleans and logs every removal (see `docs/cleaning_decisions.md`).
3. `src/03_load.py` loads a star schema (`sql/schema.sql`) into PostgreSQL.
4. `sql/analysis.sql` runs the analysis: medians by area, YoY change, rolling volume, rankings, off-plan vs ready.
5. `src/04_stats.py` fits an OLS regression on log price per sqm with robust standard errors.
6. Power BI dashboard built on the PostgreSQL tables.

## Key findings
TODO: 3 to 5 bullets, each with a number and the area/period it applies to. Only write what the data shows.

## Dashboard
TODO: add 2 to 3 screenshots and a link if you publish it.

## Limitations
TODO: Be specific, e.g. no controls for view/floor/finish; bulk-deal flag is a heuristic; association not causation.

## What I would do next
TODO: 2 to 3 ideas (add rental/Ejari data, a price forecast, a natural-language-to-SQL assistant).

## Reproduce
```bash
pip install -r requirements.txt
docker compose up -d                      # starts local PostgreSQL
# put the DLD transactions CSV at data/raw/dld_transactions.csv
python src/01_inspect.py
python src/02_clean.py
python src/03_load.py
python src/04_stats.py
```
Run the queries in `sql/analysis.sql` in psql, DBeaver, or pgAdmin.
Set `DATABASE_URL` or `RAW_FILE` as environment variables to override defaults in `config.py`.
