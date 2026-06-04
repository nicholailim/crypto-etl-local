-- Compare the latest snapshot against the previous snapshot for each coin

CREATE OR REPLACE VIEW vw_latest_vs_prev AS
WITH ranked AS (
  SELECT
    coin_id,
    symbol,
    name,
    current_price,
    market_cap,
    total_volume,
    price_change_24h,
    price_change_pct_24h,
    last_updated,
    extracted_at,
    DENSE_RANK() OVER (ORDER BY extracted_at DESC) AS run_rank
  FROM crypto_prices
)
SELECT
  l.coin_id,
  l.symbol,
  l.name,
  l.current_price AS price_latest,
  p.current_price AS price_prev,
  (l.current_price - p.current_price) AS delta_price,
  CASE WHEN p.current_price > 0 THEN ROUND(((l.current_price - p.current_price) / p.current_price) * 100.0, 6) END AS delta_pct,
  l.market_cap   AS market_cap_latest,
  p.market_cap   AS market_cap_prev,
  (l.market_cap - p.market_cap) AS delta_market_cap,
  l.total_volume AS volume_latest,
  p.total_volume AS volume_prev,
  l.extracted_at AS extracted_at_latest,
  p.extracted_at AS extracted_at_prev
FROM ranked l
LEFT JOIN ranked p
  ON p.coin_id = l.coin_id AND p.run_rank = 2
WHERE l.run_rank = 1;
