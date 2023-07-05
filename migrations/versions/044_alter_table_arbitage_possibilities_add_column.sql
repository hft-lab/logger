BEGIN;

LOCK arbitage_possibilities IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE arbitage_possibilities add column bot_launch_id varchar(64);

COMMIT;
