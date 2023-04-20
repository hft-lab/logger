CREATE TABLE IF NOT EXISTS balance_jumps (
    ts bigint NOT NULL,
    total_balance float NOT NULL,
    env varchar(64) NOT NULL default 'DEFAULT TEST'
);