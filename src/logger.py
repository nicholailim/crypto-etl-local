import logging
import os
from datetime import datetime

# Where log files will be saved
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# One log file per day, e.g. logs/etl_2026-05-24.log
log_filename = os.path.join(LOG_DIR, f"etl_{datetime.now().strftime('%Y-%m-%d')}.log")

# Create the logger — "etl" is its name, used to identify it
logger = logging.getLogger("etl")
logger.setLevel(logging.DEBUG)

# Format: timestamp  LEVEL  message
formatter = logging.Formatter(
    fmt="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Handler 1: print to terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Handler 2: save to log file
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Attach both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
