BEGIN;

LOCK balances IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balances add column current_margin float;

COMMIT;
