-- ─────────────────────────────────────────────
-- Crypto Price Analysis Queries
-- Run these in pgAdmin Query Tool
-- ─────────────────────────────────────────────


-- 1. View all coins ordered by market cap (biggest first)
--    Market cap = current_price × total supply
--    It tells us which coins are most "valuable" overall
SELECT
    name,
    symbol,
    current_price,
    market_cap,
    price_change_pct_24h
FROM crypto_prices
ORDER BY market_cap DESC;


-- 2. Top 5 best performing coins in the last 24 hours
--    "Best performing" = biggest positive % price change
SELECT
    name,
    symbol,
    current_price,
    price_change_pct_24h
FROM crypto_prices
ORDER BY price_change_pct_24h DESC
LIMIT 5;


-- 3. Top 5 worst performing coins in the last 24 hours
--    "Worst performing" = biggest negative % price change
SELECT
    name,
    symbol,
    current_price,
    price_change_pct_24h
FROM crypto_prices
ORDER BY price_change_pct_24h ASC
LIMIT 5;


-- 4. Highest trading volume coins
--    Volume = how much of this coin was traded in the last 24h
--    High volume = high market activity and liquidity
SELECT
    name,
    symbol,
    total_volume,
    current_price,
    price_change_pct_24h
FROM crypto_prices
ORDER BY total_volume DESC;


-- 5. Coins with big price drops AND high volume
--    This is more meaningful than just a price drop alone.
--    High volume + big drop = strong selling pressure
SELECT
    name,
    symbol,
    price_change_pct_24h,
    total_volume
FROM crypto_prices
WHERE price_change_pct_24h < 0
ORDER BY total_volume DESC, price_change_pct_24h ASC;


-- 6. Summary statistics across all coins
--    AVG = average, MAX = highest, MIN = lowest
SELECT
    ROUND(AVG(current_price)::NUMERIC, 2)        AS avg_price,
    MAX(current_price)                            AS highest_price,
    MIN(current_price)                            AS lowest_price,
    ROUND(AVG(price_change_pct_24h)::NUMERIC, 4) AS avg_change_pct_24h,
    SUM(total_volume)                             AS total_market_volume
FROM crypto_prices;
