BEGIN;

LOCK balance_check IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balance_check add column ask float not null default 0;
ALTER TABLE balance_check add column bid float not null default 0;
ALTER TABLE balance_check add column symbol varchar(64) not null default 'BTCUSDT';

COMMIT;
