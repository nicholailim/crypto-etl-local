import requests
import json
import os
from datetime import datetime
from src.logger import logger

# The CoinGecko API endpoint we're calling.
# This endpoint returns market data for a list of coins.
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# These are the parameters we send with the request.
# Think of them as filters/settings for what data we want back.
PARAMS = {
    "vs_currency": "usd",        # we want prices in US dollars
    "order": "market_cap_desc",  # sort by largest market cap first
    "per_page": 10,              # fetch top 10 coins (start small)
    "page": 1,
    "sparkline": False,          # we don't need sparkline chart data
    "price_change_percentage": "24h",
}

# Where to save the raw API response
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")


def fetch_coins():
    """
    Calls the CoinGecko API and returns a list of coin data as Python dicts.
    Also saves the raw response to data/raw/ as a JSON file for backup.
    """

    logger.info("Fetching data from CoinGecko API...")

    try:
        # Make the HTTP GET request to the API
        response = requests.get(API_URL, params=PARAMS, timeout=10)

        # Check if the request succeeded (status 200 = OK)
        # If something went wrong (e.g. 429 rate limit, 500 server error),
        # raise_for_status() will raise an exception so we know immediately
        response.raise_for_status()

        # Parse the JSON response body into a Python list of dicts
        data = response.json()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("CoinGecko API request timed out.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Could not connect to CoinGecko API.") from exc
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        raise RuntimeError(f"CoinGecko API returned HTTP error: {status_code}.") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError("CoinGecko API request failed.") from exc


    logger.info(f"Fetched {len(data)} coins successfully.")

    # Save raw response to data/raw/ with a timestamp in the filename
    # This gives us a backup in case the Transform step has a bug
    save_raw(data)

    return data


def save_raw(data):
    """
    Saves the raw API response as a JSON file in data/raw/.
    The filename includes a timestamp so each run creates a new file.
    """

    # Create the directory if it doesn't exist yet
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    # Build a timestamped filename, e.g. coins_2026-05-23_15-30-00.json
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"coins_{timestamp}.json"
    filepath = os.path.join(RAW_DATA_DIR, filename)

    # Write the data to the file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    logger.debug(f"Raw data saved to: {filepath}")


# This block only runs if you execute this file directly
# e.g. `python src/extract/fetch_coins.py`
# It won't run when this file is imported by main.py
if __name__ == "__main__":
    coins = fetch_coins()

    # Print the first coin's data so we can see what the API returns
    print("\nSample (first coin):")
    print(json.dumps(coins[0], indent=2))
