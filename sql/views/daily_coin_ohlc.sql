-- Daily OHLC view per coin (Open, High, Low, Close) based on extracted_at timestamps

WITH stamped AS (
  SELECT
    coin_id,
    symbol,
    name,
    current_price,
    total_volume,
    market_cap,
    extracted_at::timestamp AS extracted_at,
    date_trunc('day', extracted_at)::date AS day
  FROM crypto_prices
),
open_price AS (
  SELECT DISTINCT ON (coin_id, day)
    coin_id, day, current_price AS open_price
  FROM stamped
  ORDER BY coin_id, day, extracted_at ASC
),
close_price AS (
  SELECT DISTINCT ON (coin_id, day)
    coin_id, day, current_price AS close_price
  FROM stamped
  ORDER BY coin_id, day, extracted_at DESC
),
hi_lo AS (
  SELECT
    coin_id,
    day,
    MAX(current_price) AS high_price,
    MIN(current_price) AS low_price,
    SUM(total_volume)  AS day_volume
  FROM stamped
  GROUP BY coin_id, day
)
CREATE OR REPLACE VIEW vw_daily_coin_ohlc AS
SELECT
  o.coin_id,
  s.symbol,
  s.name,
  o.day,
  o.open_price,
  h.high_price,
  h.low_price,
  c.close_price,
  h.day_volume
FROM open_price o
JOIN close_price c USING (coin_id, day)
JOIN hi_lo h       USING (coin_id, day)
JOIN (
  SELECT DISTINCT coin_id, symbol, name FROM stamped
) s USING (coin_id);
