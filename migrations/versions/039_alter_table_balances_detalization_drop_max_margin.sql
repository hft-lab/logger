BEGIN;

ALTER TABLE balances_detalization DROP COLUMN max_margin;

COMMIT;