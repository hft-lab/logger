BEGIN;

LOCK disbalances IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE disbalances add column status varchar(64);
ALTER TABLE disbalances add column status_datetime timestamptz;
ALTER TABLE disbalances add column status_ts bigint;

COMMIT;
