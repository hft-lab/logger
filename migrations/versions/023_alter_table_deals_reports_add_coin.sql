ALTER TABLE deals_reports
ADD COLUMN coin char(16),
ADD COLUMN sell_order_id char(64),
ADD COLUMN buy_order_id char(64),
ADD COLUMN date_utc timestamptz;