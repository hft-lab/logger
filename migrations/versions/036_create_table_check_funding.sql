CREATE TABLE IF NOT EXISTS fundings (
    id UUID VARCHAR(64) NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	exchange_funding_id VARCHAR(64) NOT NULL,
	exchange VARCHAR(64) NOT NULL,
	symbol VARCHAR(64) NOT NULL,
	amount FLOAT NOT NULL,
	asset VARCHAR(64) NOT NULL,
	position_coin FLOAT NOT NULL,
	price FLOAT NOT NULL
);
