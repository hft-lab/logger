CREATE TABLE IF NOT EXISTS ping_logging (
	server_name VARCHAR(64) NOT NULL,
	exchange_name VARCHAR(64) NOT NULL,
	status_of_ping ping_status_enum NOT NULL,
    ts_of_request bigint NOT NULL,
    ts_from_response bigint NOT NULL,
    ts_received_response bigint NOT NULL
);