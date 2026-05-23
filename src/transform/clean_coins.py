import pandas as pd


def clean_coins(raw_data):
    """
    Takes the raw list of coin dicts from the API and returns a
    clean pandas DataFrame with only the columns we need.

    Steps:
    1. Load raw data into a DataFrame
    2. Select only the columns we want
    3. Rename columns to match our database schema
    4. Convert last_updated from string to datetime
    5. Drop any rows with missing critical data
    """

    # Step 1: Load the raw list of dicts into a pandas DataFrame.
    # A DataFrame is like a table — rows and columns, similar to Excel.
    df = pd.DataFrame(raw_data)

    print(f"Raw data shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Step 2: Select only the columns we actually need.
    # Everything else gets dropped here.
    df = df[[
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_24h",
        "price_change_percentage_24h",
        "last_updated",
    ]]

    # Step 3: Rename columns to match our database schema.
    # Key changes:
    #   "id" → "coin_id"  (because "id" is our DB's own primary key)
    #   "price_change_percentage_24h" → "price_change_pct_24h" (shorter)
    df = df.rename(columns={
        "id": "coin_id",
        "price_change_percentage_24h": "price_change_pct_24h",
    })

    # Step 4: Convert last_updated from a string to a proper datetime.
    # The API gives us: "2026-05-23T07:55:08.003Z"
    # pd.to_datetime() parses that string into a real datetime object.
    # utc=True tells pandas the time is in UTC timezone.
    df["last_updated"] = pd.to_datetime(df["last_updated"], utc=True)

    # Step 5: Drop rows where critical fields are missing (NaN).
    # We don't want to insert incomplete records into the database.
    df = df.dropna(subset=["coin_id", "current_price", "market_cap"])

    print(f"Clean data shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    return df


# Run this file directly to test the transform step in isolation
if __name__ == "__main__":
    import json
    import os
    import glob

    # Find the most recently saved raw file
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    files = glob.glob(os.path.join(raw_dir, "coins_*.json"))

    if not files:
        print("No raw data files found. Run fetch_coins.py first.")
    else:
        latest_file = max(files)  # most recent by filename (timestamp sorts alphabetically)
        print(f"Loading: {latest_file}")

        with open(latest_file) as f:
            raw_data = json.load(f)

        clean_df = clean_coins(raw_data)

        print("\nSample cleaned data:")
        print(clean_df.head())
        print("\nData types:")
        print(clean_df.dtypes)
