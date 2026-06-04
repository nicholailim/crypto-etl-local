import psycopg2
import os
from dotenv import load_dotenv
from src.logger import logger

# Load the variables from our .env file into the environment.
# After this line, os.getenv() can read DB_HOST, DB_PASSWORD, etc.
load_dotenv()


def get_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    Credentials are read from environment variables (our .env file).
    We never hardcode passwords in code.
    """
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection


def insert_coins(df):
    """
    Takes a clean pandas DataFrame and inserts each row into
    the crypto_prices table in PostgreSQL.
    """

    # Open a connection to the database
    conn = get_connection()

    # A cursor lets us execute SQL commands
    cursor = conn.cursor()

    logger.info(f"Inserting {len(df)} rows into crypto_prices...")

    # Ensure a unique constraint exists (coin_id, extracted_at) to prevent exact duplicates in a run
    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE schemaname = 'public' AND indexname = 'uq_coin_extracted_at') THEN
                BEGIN
                    -- create a unique index that effectively enforces one row per coin per run timestamp
                    EXECUTE 'CREATE UNIQUE INDEX uq_coin_extracted_at ON crypto_prices(coin_id, extracted_at)';
                END;
            END IF;
        END$$;
    """)

    conflicts = 0

    # Loop through each row in the DataFrame and insert it; ignore exact duplicates for same run timestamp
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO crypto_prices (
                coin_id,
                symbol,
                name,
                current_price,
                market_cap,
                total_volume,
                price_change_24h,
                price_change_pct_24h,
                last_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (coin_id, extracted_at) DO NOTHING
        """, (
            row["coin_id"],
            row["symbol"],
            row["name"],
            row["current_price"],
            row["market_cap"],
            row["total_volume"],
            row["price_change_24h"],
            row["price_change_pct_24h"],
            row["last_updated"],
        ))
        # track if nothing was inserted for this row
        if cursor.rowcount == 0:
            conflicts += 1

    # commit() saves all the inserts to the database permanently.
    # Without this, the inserts are temporary and lost when the connection closes.
    conn.commit()

    if conflicts:
        logger.warning(f"{conflicts} row(s) skipped due to duplicate (coin_id, extracted_at).")
    logger.info(f"Successfully inserted {len(df) - conflicts} rows.")

    # Always close the cursor and connection when done
    cursor.close()
    conn.close()


# Test this file directly
if __name__ == "__main__":
    from src.extract.fetch_coins import fetch_coins
    from src.transform.clean_coins import clean_coins

    raw = fetch_coins()
    clean_df = clean_coins(raw)
    insert_coins(clean_df)
    print("Load step complete!")
