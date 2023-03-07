BEGIN;

LOCK balance_check IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_balance_check_ts_was_sent ON balance_check USING btree (ts, was_sent);

COMMIT;