BEGIN;

LOCK balances_detalization IN ROW EXCLUSIVE MODE NOWAIT;

ALTER TABLE balances_detalization add column available_for_buy float;
ALTER TABLE balances_detalization add column available_for_sell float;
ALTER TABLE balances_detalization add column grand_parent_id uuid;

COMMIT;
