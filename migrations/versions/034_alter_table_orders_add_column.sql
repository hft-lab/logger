BEGIN;

LOCK orders IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE orders add column datetime_update timestamptz;
ALTER TABLE orders add column ts_update bigint;

COMMIT;
