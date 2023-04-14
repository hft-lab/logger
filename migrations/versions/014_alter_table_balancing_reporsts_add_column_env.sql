BEGIN;

LOCK balancing_reports IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balancing_reports add column env varchar(64) NOT NULL default 'DEFAULT TEST';

COMMIT;
