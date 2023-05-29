CREATE TABLE IF NOT EXISTS disbalances (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	coin_name VARCHAR(64) NOT NULL,
	position_coin FLOAT NOT NULL DEFAULT 10,
	position_usd FLOAT NOT NULL,
	price FLOAT NOT NULL
);