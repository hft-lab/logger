BEGIN;

LOCK balancing_reports IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balancing_reports add column coin varchar(64) default 0;

COMMIT;
