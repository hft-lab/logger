CREATE TABLE IF NOT EXISTS bot_config (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	context context_enum NOT NULL,
	exchange_1 VARCHAR(64) NOT NULL,
	exchange_2 VARCHAR(64) NOT NULL,
	coin VARCHAR(64) NOT NULL,
	bots_quantity INT NOT NULL,
	shift_use_flag INT,
	target_profit FLOAT,
	order_delay FLOAT,
	max_order_usd FLOAT,
	max_leverage FLOAT,
	pause_flag INT DEFAULT NULL,
	api_secret_encrypted VARCHAR(64) NOT NULL
);
