CREATE TABLE IF NOT EXISTS balance_detalization (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	context  VARCHAR(64) NOT NULL,
    parent_id UUID NOT NULL,
	exchange VARCHAR(64) NOT NULL,
	side VARCHAR(64) NOT NULL,
	symbol VARCHAR(64) NOT NULL,
	max_margin FLOAT NOT NULL DEFAULT 10,
	current_margin FLOAT NOT NULL,
	position_coin FLOAT NOT NULL,
	position_usd FLOAT NOT NULL,
	entry_price FLOAT NOT NULL,
	mark_price FLOAT NOT NULL
);