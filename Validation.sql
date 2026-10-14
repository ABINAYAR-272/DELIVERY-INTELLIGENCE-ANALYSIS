USE delivery_intelligence;

-- Dataset size and order-item grain.
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT `Order Id`) AS unique_orders,
    COUNT(DISTINCT `Order Item Id`) AS unique_order_items,
    COUNT(DISTINCT `Customer Id`) AS unique_customers
FROM delivery_data;

SELECT
    COUNT(*) AS total_records,

    SUM(`Order Id` IS NULL) AS missing_order_id,
    SUM(`Order Item Id` IS NULL) AS missing_order_item_id,
    SUM(`Customer Id` IS NULL) AS missing_customer_id,
    SUM(`Market` IS NULL OR TRIM(`Market`) = '') AS missing_market,
    SUM(`Order Region` IS NULL OR TRIM(`Order Region`) = '') AS missing_region,
    SUM(`Shipping Mode` IS NULL OR TRIM(`Shipping Mode`) = '')
        AS missing_shipping_mode,
    SUM(`Delivery Status` IS NULL OR TRIM(`Delivery Status`) = '')
        AS missing_delivery_status,
    SUM(`Days for shipping (real)` IS NULL) AS missing_actual_days,
    SUM(`Days for shipment (scheduled)` IS NULL) AS missing_scheduled_days
FROM delivery_data;

SELECT
    `Delivery Status`,
    `Late_delivery_risk`,
    COUNT(*) AS record_count
FROM delivery_data
GROUP BY `Delivery Status`, `Late_delivery_risk`
ORDER BY `Delivery Status`, `Late_delivery_risk`;

SELECT
    `Delivery Status`,
    CASE
        WHEN `Days for shipping (real)` IS NULL
          OR `Days for shipment (scheduled)` IS NULL
            THEN 'Unknown'
        WHEN `Days for shipping (real)`
           > `Days for shipment (scheduled)` THEN 'Late'
        WHEN `Days for shipping (real)`
           = `Days for shipment (scheduled)` THEN 'On schedule'
        ELSE 'Early'
    END AS calculated_timing,
    COUNT(*) AS record_count
FROM delivery_data
GROUP BY
    `Delivery Status`,
    calculated_timing
ORDER BY record_count DESC;