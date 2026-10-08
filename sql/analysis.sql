-- PostgreSQL analysis queries. Bulk/portfolio deals are excluded (NOT f.is_bulk).

-- 1. Median price per sqm by area and year
SELECT a.area_name, d.year,
       COUNT(*) AS n_sales,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_per_sqm) AS median_psqm
FROM fact_transactions f
JOIN dim_area a ON a.area_id = f.area_id
JOIN dim_date d ON d.date_id = f.date_id
WHERE NOT f.is_bulk
GROUP BY a.area_name, d.year
HAVING COUNT(*) >= 30
ORDER BY a.area_name, d.year;

-- 2. Year-over-year change in median price per sqm, by area (window function)
WITH yearly AS (
    SELECT a.area_name, d.year,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_per_sqm) AS median_psqm,
           COUNT(*) AS n_sales
    FROM fact_transactions f
    JOIN dim_area a ON a.area_id = f.area_id
    JOIN dim_date d ON d.date_id = f.date_id
    WHERE NOT f.is_bulk
    GROUP BY a.area_name, d.year
    HAVING COUNT(*) >= 30
)
SELECT area_name, year, ROUND(median_psqm) AS median_psqm,
       ROUND(100.0 * (median_psqm / LAG(median_psqm) OVER (PARTITION BY area_name ORDER BY year) - 1), 1) AS yoy_pct
FROM yearly
ORDER BY area_name, year;

-- 3. Monthly sales volume with a rolling 3-month average
WITH monthly AS (
    SELECT d.year, d.month, COUNT(*) AS n_sales
    FROM fact_transactions f JOIN dim_date d ON d.date_id = f.date_id
    WHERE NOT f.is_bulk
    GROUP BY d.year, d.month
)
SELECT year, month, n_sales,
       ROUND(AVG(n_sales) OVER (ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS rolling_3m_avg
FROM monthly ORDER BY year, month;

-- 4. Rank areas by liquidity (volume) and show price level
SELECT a.area_name, COUNT(*) AS n_sales,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS volume_rank,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_per_sqm)) AS median_psqm
FROM fact_transactions f JOIN dim_area a ON a.area_id = f.area_id
WHERE NOT f.is_bulk
GROUP BY a.area_name
ORDER BY n_sales DESC
LIMIT 25;

-- 5. Off-plan vs ready price level by area
SELECT a.area_name, p.reg_type, COUNT(*) AS n_sales,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.price_per_sqm)) AS median_psqm
FROM fact_transactions f
JOIN dim_area a ON a.area_id = f.area_id
JOIN dim_property p ON p.property_id = f.property_id
WHERE NOT f.is_bulk
GROUP BY a.area_name, p.reg_type
HAVING COUNT(*) >= 30
ORDER BY a.area_name, p.reg_type;
