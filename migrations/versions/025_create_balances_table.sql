CREATE TABLE IF NOT EXISTS balances (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	context context_enum NOT NULL,
    parent_id UUID NOT NULL,
	exchange VARCHAR(64) NOT NULL,
	exchange_balance FLOAT NOT NULL,
	available_for_buy FLOAT NOT NULL,
	available_for_sell FLOAT NOT NULL,
	exchange_available_for_buy FLOAT NOT NULL,
	exchange_available_for_sell FLOAT NOT NULL,
	was_sent BOOLEAN DEFAULT FALSE,
	env VARCHAR(64) NOT NULL,
	chat_id INT8 NOT NULL,
	bot_token VARCHAR(64) NOT NULL
);