BEGIN;

LOCK balances IN EXCLUSIVE MODE NOWAIT;

ALTER TABLE balances
	drop column exchange_available_for_buy,
	drop column exchange_available_for_sell;

COMMIT;