BEGIN;

LOCK ping_logging IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_ping_logging_server_name_exchange_name_status_of_ping ON ping_logging USING btree (server_name, exchange_name, status_of_ping);
CREATE INDEX ix_ping_logging_exchange_name_status_of_ping ON ping_logging USING btree (exchange_name, status_of_ping);
CREATE INDEX ix_ping_logging_status_of_ping ON ping_logging USING btree (status_of_ping);
CREATE INDEX ix_ping_logging_ts_of_request ON ping_logging USING btree (ts_of_request DESC);
CREATE INDEX ix_ping_logging_ts_from_response ON ping_logging USING btree (ts_from_response DESC);
CREATE INDEX ix_ping_logging_ts_received_response ON ping_logging USING btree (ts_received_response DESC);

COMMIT;