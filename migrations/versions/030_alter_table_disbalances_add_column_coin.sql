BEGIN;

LOCK disbalances IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE disbalances add column threshold float default 0;

COMMIT;
