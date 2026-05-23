# main.py — Entry point for the ETL pipeline
# This is where the Extract → Transform → Load steps will be orchestrated.
# We'll build each step one at a time.

from extract.fetch_coins import fetch_coins
from transform.clean_coins import clean_coins
from load.insert_coins import insert_coins


def run_pipeline():
    print("=" * 40)
    print("ETL Pipeline starting...")
    print("=" * 40)

    # Step 1: Extract — call the API, save raw JSON
    raw_data = fetch_coins()

    # Step 2: Transform — clean, rename, convert types
    clean_data = clean_coins(raw_data)

    # Step 3: Load — insert into PostgreSQL
    insert_coins(clean_data)

    print("=" * 40)
    print("Pipeline complete.")
    print("=" * 40)


if __name__ == "__main__":
    run_pipeline()
