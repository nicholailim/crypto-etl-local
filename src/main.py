# main.py — Entry point for the ETL pipeline
# This is where the Extract → Transform → Load steps will be orchestrated.
# We'll build each step one at a time.

from src.extract.fetch_coins import fetch_coins
from src.transform.clean_coins import clean_coins
from src.load.insert_coins import insert_coins
from src.logger import logger


def run_pipeline():
    logger.info("=" * 40)
    logger.info("ETL Pipeline starting...")
    logger.info("=" * 40)

    # Step 1: Extract — call the API, save raw JSON
    logger.info("[EXTRACT] Starting...")
    try:
        raw_data = fetch_coins()
        logger.info("[EXTRACT] Done.")
    except Exception as e:
        logger.error(f"[EXTRACT] FAILED — {e}")
        logger.error("Pipeline stopped.")
        return

    # Step 2: Transform — clean, rename, convert types
    logger.info("[TRANSFORM] Starting...")
    try:
        clean_data = clean_coins(raw_data)
        logger.info("[TRANSFORM] Done.")
    except Exception as e:
        logger.error(f"[TRANSFORM] FAILED — {e}")
        logger.error("Pipeline stopped.")
        return

    # Step 3: Load — insert into PostgreSQL
    logger.info("[LOAD] Starting...")
    try:
        insert_coins(clean_data)
        logger.info("[LOAD] Done.")
    except Exception as e:
        logger.error(f"[LOAD] FAILED — {e}")
        logger.error("Pipeline stopped.")
        return

    logger.info("=" * 40)
    logger.info("Pipeline complete.")
    logger.info("=" * 40)


if __name__ == "__main__":
    run_pipeline()
