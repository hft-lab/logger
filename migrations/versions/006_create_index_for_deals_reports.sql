BEGIN;

LOCK deals_reports IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_deals_reports_ts_was_sent ON deals_reports USING btree (ts, was_sent);

COMMIT;