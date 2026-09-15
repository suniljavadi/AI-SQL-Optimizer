CREATE TABLE IF NOT EXISTS customers (customer_id SERIAL PRIMARY KEY, name TEXT NOT NULL, region TEXT NOT NULL, created_at DATE NOT NULL);
CREATE TABLE IF NOT EXISTS orders (order_id SERIAL PRIMARY KEY, customer_id INT NOT NULL REFERENCES customers(customer_id), order_date DATE NOT NULL, total_amount NUMERIC(12,2) NOT NULL, status TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS ix_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS ix_orders_order_date ON orders(order_date);
INSERT INTO customers(name, region, created_at) SELECT 'Customer ' || n, CASE WHEN n % 2 = 0 THEN 'East' ELSE 'West' END, DATE '2024-01-01' + n FROM generate_series(1, 100) n ON CONFLICT DO NOTHING;
INSERT INTO orders(customer_id, order_date, total_amount, status) SELECT (n % 100) + 1, DATE '2026-01-01' + (n % 365), (n * 13.25)::numeric(12,2), CASE WHEN n % 3 = 0 THEN 'shipped' ELSE 'pending' END FROM generate_series(1, 1000) n ON CONFLICT DO NOTHING;
