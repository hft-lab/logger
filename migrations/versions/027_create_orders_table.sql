CREATE TABLE IF NOT EXISTS orders (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	context VARCHAR(64) NOT NULL,
    parent_id UUID NOT NULL,
	exchange_order_id VARCHAR(64) NOT NULL,
	type VARCHAR(8) NOT NULL,
	status VARCHAR(64) NOT NULL,
	exchange VARCHAR(64) NOT NULL,
	side VARCHAR(64) NOT NULL,
	symbol VARCHAR(64) NOT NULL,
	expect_price FLOAT NOT NULL,
	expect_amount_coin FLOAT NOT NULL,
	expect_amount_usd FLOAT NOT NULL,
	expect_fee FLOAT NOT NULL,
	factual_price FLOAT NOT NULL,
	factual_amount_coin FLOAT NOT NULL,
	factual_amount_usd FLOAT NOT NULL,
	factual_fee FLOAT NOT NULL,
	order_place_time FLOAT NOT NULL,
	env VARCHAR(64) NOT NULL
);