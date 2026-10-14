WITH region_performance AS (
    SELECT
        `Market` AS market,
        `Order Region` AS order_region,
        COUNT(*) AS shipment_records,
        SUM(
            CASE
                WHEN `Days for shipping (real)`
                   > `Days for shipment (scheduled)`
                THEN 1 ELSE 0
            END
        ) AS late_records,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN `Days for shipping (real)`
                       > `Days for shipment (scheduled)`
                    THEN 1 ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS late_rate_pct
    FROM delivery_data
    WHERE `Days for shipping (real)` IS NOT NULL
      AND `Days for shipment (scheduled)` IS NOT NULL
      AND `Market` IS NOT NULL
      AND `Order Region` IS NOT NULL
    GROUP BY `Market`, `Order Region`
    HAVING COUNT(*) >= 100
),
ranked_regions AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            PARTITION BY market
            ORDER BY late_rate_pct DESC
        ) AS risk_rank
    FROM region_performance
)
SELECT *
FROM ranked_regions
WHERE risk_rank <= 3
ORDER BY market, risk_rank, shipment_records DESC;