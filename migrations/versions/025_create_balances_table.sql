CREATE TABLE IF NOT EXISTS balances (
    id uuid NOT NULL UNIQUE,
    dt timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	exchange_name VARCHAR(64) NOT NULL,
	total_balance FLOAT NOT NULL,
	pos FLOAT NOT NULL,
	available_for_buy FLOAT NOT NULL,
	available_for_sell FLOAT NOT NULL,
	was_sent BOOLEAN default FALSE
);