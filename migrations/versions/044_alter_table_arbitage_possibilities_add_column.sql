BEGIN;

LOCK arbitrage_possibilities IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE arbitrage_possibilities add column bot_launch_id varchar(64);

COMMIT;
