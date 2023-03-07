BEGIN;

LOCK balancing_reports IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_balancing_reports_ts_was_sent ON balancing_reports USING btree (ts, was_sent);

COMMIT;