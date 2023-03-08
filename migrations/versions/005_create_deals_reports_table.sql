CREATE TABLE IF NOT EXISTS deals_reports (
	ts BIGINT NOT NULL,
	sell_exch VARCHAR(64) NOT NULL,
	buy_exch VARCHAR(64) NOT NULL,
	sell_px FLOAT NOT NULL,
    expect_sell_px FLOAT NOT NULL,
    buy_px FLOAT NOT NULL,
    expect_buy_px FLOAT NOT NULL,
    amount_USD FLOAT NOT NULL,
    amount_coin FLOAT NOT NULL,
    profit_USD FLOAT NOT NULL,
    profit_relative FLOAT NOT NULL,
    fee_sell FLOAT NOT NULL,
    fee_buy FLOAT NOT NULL,
    long_side VARCHAR(64) NOT NULL,
    sell_ob_ask FLOAT NOT NULL,
    buy_ob_bid FLOAT NOT NULL,
    deal_time FLOAT NOT NULL,
    time_parser FLOAT NOT NULL,
    time_choose FLOAT NOT NULL,
    was_sent BOOLEAN default FALSE
);