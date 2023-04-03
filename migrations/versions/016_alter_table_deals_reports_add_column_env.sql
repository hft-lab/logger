BEGIN;

LOCK deals_reports IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE deals_reports add column env varchar(64) NOT NULL default 'DEFAULT TEST';

COMMIT;
