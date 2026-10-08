# Cleaning decisions

Row counts come from `docs/cleaning_log.csv`, produced by `src/02_clean.py`.

| Step | Rows after | Rows removed | Why |
|------|-----------:|-------------:|-----|
| Raw file | 898,413 | | All transaction types, many decades |
| Unparseable dates | 898,413 | 0 | Dates are ISO format (YYYY-MM-DD); none failed to parse |
| Keep dates from 2019-01-01 | 562,199 | 336,214 | Analysis window; also removes a few impossible dates (such as years 1420 and 1966) |
| Sales transactions only | 438,172 | 124,027 | Mortgages and gifts are not market sales |
| Keep three sale procedures | 427,025 | 11,147 | Kept Sell - Pre registration, Sell, and Delayed Sell (see below) |
| Residential flats and villas only | 349,482 | 77,543 | Offices, shops, hotel rooms, and similar have different price per sqm dynamics |
| Missing or non-positive value or area | 349,482 | 0 | None found |
| Duplicate transaction IDs | 349,482 | 0 | None found |
| Extreme price per sqm outliers | 348,789 | 693 | Removed where |z| > 4 on log price per sqm within property sub type |

Final cleaned sample: **348,789 sales**. The regression uses 346,882 after excluding flagged bulk deals.

## Procedure whitelist

Procedures were compared on median price per sqm and on whether they were off-plan or existing. "Sell - Pre registration" is always off-plan (median about 18,200 AED per sqm), while "Sell" (about 12,300) and "Delayed Sell" (about 15,100) are always existing. The seven procedures I dropped (development registrations, payment plans, lease-to-own, and similar) total about 6,900 rows, roughly 2% of the sample, and mostly show much lower median prices (about 6,600 to 11,700 per sqm). I could not confirm exactly what they represent, so excluding them is a conservative judgment call.

"Delayed Sell" sits between the other two on price and I do not know exactly what it covers. The regression was re-run without it as a sensitivity check. The year effects barely moved, and the off-plan premium rose from about 38% to about 46%.

## Bulk and portfolio deals

`is_bulk` flags rows where 10 or more transactions share the same date, area, and value, which usually indicates a portfolio or bulk registration. It flagged 1,907 rows (about 0.5%). These rows are kept in the database but excluded from the SQL analysis and the regression. The rule is a heuristic that I have not validated against another source, and I have not tested how the results change if the flagged rows are included.

## Other decisions

- Price per sqm is recomputed as value divided by area, not taken from the source's own column.
- The off-plan and existing labels come from the source's registration type, which matches the procedure exactly.
- Areas outside the 25 busiest are grouped as "Other" in the regression. Rooms outside the 8 most common are grouped as "Other".

## Known limitations

- About two-thirds of the cleaned sample is off-plan, so results mostly describe off-plan primary sales.
- Area and project names are official DLD names, not marketing names.
- 2026 is a partial year (to 2 October).
