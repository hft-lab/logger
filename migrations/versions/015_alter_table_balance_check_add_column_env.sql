BEGIN;

LOCK balance_check IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balance_check add column env varchar(64) NOT NULL;

COMMIT;
