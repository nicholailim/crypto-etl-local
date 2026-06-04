-- Latest snapshot view and helpful indexes
 
CREATE OR REPLACE VIEW vw_latest_snapshot AS
SELECT
  cp.coin_id,
  cp.symbol,
  cp.name,
  cp.current_price,
  cp.market_cap,
  cp.total_volume,
  cp.price_change_24h,
  cp.price_change_pct_24h,
  cp.last_updated,
  cp.extracted_at
FROM crypto_prices cp
WHERE cp.extracted_at = (SELECT MAX(extracted_at) FROM crypto_prices);
 
-- Indexes to speed up snapshot filters and time-based queries
CREATE INDEX IF NOT EXISTS idx_crypto_prices_extracted_at
  ON crypto_prices(extracted_at);
 
CREATE INDEX IF NOT EXISTS idx_crypto_prices_coin_id_extracted_at
  ON crypto_prices(coin_id, extracted_at);