CREATE TABLE IF NOT EXISTS bot_config (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	exchange_1 VARCHAR(64) NOT NULL,
	exchange_2 VARCHAR(64) NOT NULL,
	coin VARCHAR(64) NOT NULL,
	env VARCHAR(64) NOT NULL,
	fee_exchange_1 FLOAT NOT NULL,
	fee_exchange_2 FLOAT NOT NULL,
	shift FLOAT NOT NULL,
	order_delay FLOAT NOT NULL,
	max_order_usd FLOAT NOT NULL,
	max_leverage FLOAT NOT NULL
);
