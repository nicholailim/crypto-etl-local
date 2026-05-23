-- Creates the main table for storing cryptocurrency data
-- Run this once to set up your database schema

CREATE TABLE IF NOT EXISTS crypto_prices (
    id                   SERIAL PRIMARY KEY,
    coin_id              VARCHAR(50),       -- e.g. "bitcoin"
    symbol               VARCHAR(20),       -- e.g. "btc"
    name                 VARCHAR(100),      -- e.g. "Bitcoin"
    current_price        NUMERIC,           -- price in USD
    market_cap           NUMERIC,           -- total market cap (NUMERIC safer than BIGINT for crypto)
    total_volume         NUMERIC,           -- 24h trading volume
    price_change_24h     NUMERIC,           -- absolute price change in last 24h
    price_change_pct_24h NUMERIC,           -- % price change in last 24h
    last_updated         TIMESTAMP,         -- when the API last updated this coin's data
    extracted_at         TIMESTAMP DEFAULT NOW()  -- when our pipeline fetched this row
);
