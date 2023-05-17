CREATE TABLE IF NOT EXISTS arbitrage_possibilities (
    id UUID NOT NULL UNIQUE,
    datetime timestamptz NOT NULL,
	ts BIGINT NOT NULL,
	buy_exchange VARCHAR(64) NOT NULL,
	sell_exchange VARCHAR(64) NOT NULL,
    symbol VARCHAR(64) NOT NULL,
    buy_order_id VARCHAR(64) NOT NULL,
    sell_order_id VARCHAR(64) NOT NULL,
    available_for_buy FLOAT NOT NULL,
    max_sell_vol FLOAT NOT NULL,
    expect_buy_price FLOAT NOT NULL,
    expect_sell_price FLOAT NOT NULL,
    expect_amount_usd FLOAT NOT NULL,
    expect_amount_coin FLOAT NOT NULL,
    expect_profit_usd FLOAT NOT NULL,
    expect_profit_relative FLOAT NOT NULL,
    expect_fee_buy FLOAT NOT NULL,
    expect_fee_sell FLOAT NOT NULL,
    time_parser FLOAT NOT NULL,
    time_choose FLOAT NOT NULL,
	was_sent BOOLEAN DEFAULT FALSE,
	chat_id INT8 NOT NULL,
	bot_token VARCHAR(64) NOT NULL
);