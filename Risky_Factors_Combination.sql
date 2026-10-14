SELECT
    `Market`,
    `Order Region`,
    `Shipping Mode`,
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
  AND `Shipping Mode` IS NOT NULL
GROUP BY `Market`, `Order Region`, `Shipping Mode`
HAVING COUNT(*) >= 100
ORDER BY late_rate_pct DESC, shipment_records DESC;

SELECT
    `Order Region`,
    `Category Name`,
    COUNT(*) AS shipment_records,
    ROUND(
        100.0 * AVG(
            CASE
                WHEN `Days for shipping (real)`
                   > `Days for shipment (scheduled)`
                THEN 1.0 ELSE 0.0
            END
        ),
        2
    ) AS late_rate_pct,
    ROUND(
        AVG(
            `Days for shipping (real)`
            - `Days for shipment (scheduled)`
        ),
        2
    ) AS average_days_vs_promise
FROM delivery_data
WHERE `Days for shipping (real)` IS NOT NULL
  AND `Days for shipment (scheduled)` IS NOT NULL
  AND `Order Region` IS NOT NULL
  AND `Category Name` IS NOT NULL
GROUP BY `Order Region`, `Category Name`
HAVING COUNT(*) >= 100
ORDER BY late_rate_pct DESC, shipment_records DESC;