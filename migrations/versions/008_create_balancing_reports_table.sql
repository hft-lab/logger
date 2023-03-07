CREATE TABLE IF NOT EXISTS balancing_reports (
	ts BIGINT NOT NULL,
	exchange_name VARCHAR(64) NOT NULL,
	side side_enum NOT NULL,
	price FLOAT NOT NULL,
	taker_fee FLOAT NOT NULL,
	position_gap FLOAT NOT NULL,
	size_usd FLOAT NOT NULL,
	was_sent BOOLEAN default FALSE
);