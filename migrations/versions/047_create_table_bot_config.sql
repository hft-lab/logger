CREATE TABLE IF NOT EXISTS bot_config (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	context context_enum NOT NULL,
	exchange_1 VARCHAR(64) NOT NULL,
	exchange_2 VARCHAR(64) NOT NULL,
	coin VARCHAR(64) NOT NULL,
	bots_quantity INT NOT NULL,
	shift_use_flag INT NOT NULL,
	target_profit FLOAT NOT NULL,
	order_delay FLOAT NOT NULL,
	max_order_usd FLOAT NOT NULL,
	max_leverage FLOAT NOT NULL,
	pause_flag INT DEFAULT NULL,
	api_secret_encrypted VARCHAR(64) NOT NULL
);
