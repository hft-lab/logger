BEGIN;

LOCK arbitrage_possibilities IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE arbitrage_possibilities add column status varchar(64);
ALTER TABLE arbitrage_possibilities add column status_datetime timestamptz;
ALTER TABLE arbitrage_possibilities add column status_ts bigint;

COMMIT;
