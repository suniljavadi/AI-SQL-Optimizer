-- Synthetic examples covering joins, aggregations, subqueries, CTEs, windows, dates, sorting, filtering.
SELECT * FROM orders WHERE YEAR(order_date) = 2026;
SELECT c.region, COUNT(*) FROM orders o JOIN customers c ON c.customer_id = o.customer_id GROUP BY c.region;
SELECT * FROM orders WHERE customer_id IN (SELECT customer_id FROM customers WHERE region = 'East');
WITH recent AS (SELECT * FROM orders WHERE order_date >= '2026-01-01') SELECT customer_id, SUM(total_amount) FROM recent GROUP BY customer_id;
SELECT order_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn FROM orders;
