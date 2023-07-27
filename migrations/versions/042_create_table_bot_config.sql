CREATE TABLE IF NOT EXISTS bot_config (
    id UUID UNIQUE,
    datetime timestamptz,
	ts BIGINT,
	exchange_1 VARCHAR(64),
	exchange_2 VARCHAR(64),
	coin VARCHAR(64),
	env VARCHAR(64),
	target_profit FLOAT,
	fee_exchange_1 FLOAT,
	fee_exchange_2 FLOAT,
	shift FLOAT,
	orders_delay FLOAT,
	max_order_usd FLOAT,
	max_leverage FLOAT
);
