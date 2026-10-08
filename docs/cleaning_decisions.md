# Cleaning decisions

Fill this in after running `src/02_clean.py`, using `docs/cleaning_log.csv` for the numbers.
For each step: what you removed, how many rows, and WHY. Recruiters read this to judge your judgment.

| Step | Rows removed | Why |
|------|--------------|-----|
| Unparseable dates | | |
| Outside analysis window | | |
| Non-sales transactions | | |
| Missing / non-positive value or area | | |
| Duplicate transaction IDs | | |
| Extreme price/sqm outliers (|z| > 4 by sub type) | | |

## Bulk / portfolio deals
The `is_bulk` flag is a heuristic (10+ rows with the same date, area, and value). Describe what you
checked to validate it, how many rows it flags, and how results change when they are included vs excluded.

## Known limitations
- 
