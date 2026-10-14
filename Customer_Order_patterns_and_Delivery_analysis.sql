WITH customer_orders AS (
    SELECT DISTINCT
        `Customer Id` AS customer_id,
        `Order Id` AS order_id
    FROM delivery_data
    WHERE `Customer Id` IS NOT NULL
      AND `Order Id` IS NOT NULL
),
customer_frequency AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders
    FROM customer_orders
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN total_orders = 1 THEN '1 order'
        WHEN total_orders BETWEEN 2 AND 5 THEN '2-5 orders'
        WHEN total_orders BETWEEN 6 AND 10 THEN '6-10 orders'
        ELSE '11+ orders'
    END AS customer_order_group,
    COUNT(*) AS customers,
    ROUND(AVG(total_orders), 2) AS average_orders_per_customer
FROM customer_frequency
GROUP BY customer_order_group
ORDER BY MIN(total_orders);

WITH order_level AS (
    SELECT
        `Customer Id` AS customer_id,
        `Order Id` AS order_id,
        MAX(`Days for shipping (real)`) AS actual_days,
        MAX(`Days for shipment (scheduled)`) AS scheduled_days
    FROM delivery_data
    WHERE `Customer Id` IS NOT NULL
      AND `Order Id` IS NOT NULL
    GROUP BY `Customer Id`, `Order Id`
),
customer_performance AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(
            CASE
                WHEN actual_days IS NOT NULL
                 AND scheduled_days IS NOT NULL
                 AND actual_days > scheduled_days
                THEN 1 ELSE 0
            END
        ) AS late_orders,
        COUNT(
            CASE
                WHEN actual_days IS NOT NULL
                 AND scheduled_days IS NOT NULL
                THEN 1
            END
        ) AS orders_with_valid_durations
    FROM order_level
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_orders,
    late_orders,
    orders_with_valid_durations,
    ROUND(
        100.0 * late_orders
        / NULLIF(orders_with_valid_durations, 0),
        2
    ) AS late_order_rate_pct
FROM customer_performance
WHERE total_orders >= 2
ORDER BY late_order_rate_pct DESC, total_orders DESC;