CREATE TABLE IF NOT EXISTS balance_check (
	ts BIGINT NOT NULL,
	exchange_name VARCHAR(64) NOT NULL,
	total_balance FLOAT NOT NULL,
	pos FLOAT NOT NULL,
	available_for_buy FLOAT NOT NULL,
	available_for_sell FLOAT NOT NULL,
	was_sent BOOLEAN default FALSE
);