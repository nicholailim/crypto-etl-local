# Crypto ETL Pipeline — Local (Non-Cloud)

A beginner-to-intermediate Data Engineering project built with Python and PostgreSQL.

## Goal
Fetch cryptocurrency data from a public API, clean and transform it, store it in a local PostgreSQL database, and run SQL analysis on it.

## Tech Stack
- **Python** — scripting and pipeline logic
- **PostgreSQL** — local data warehouse
- **psycopg2** — Python-PostgreSQL connector
- **requests** — HTTP API calls
- **pandas** — data transformation
- **python-dotenv** — environment variable management

## Project Structure
```
crypto-etl-local/
├── src/
│   ├── extract/        # Pull data from APIs
│   ├── transform/      # Clean and reshape data
│   ├── load/           # Insert data into PostgreSQL
│   └── utils/          # Shared helpers (logging, DB connection)
├── sql/
│   ├── create_tables/  # DDL scripts to create tables
│   └── analysis/       # SQL queries for analysis
├── data/
│   ├── raw/            # Raw API responses (JSON)
│   └── processed/      # Cleaned data (CSV/JSON)
├── tests/              # Unit tests
├── logs/               # Pipeline run logs
├── notebooks/          # Jupyter notebooks for exploration
├── .env.example        # Environment variable template
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup
1. Clone the repo and navigate to the project folder
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your PostgreSQL credentials
6. Run the table creation script: `psql -U postgres -f sql/create_tables/coins.sql`
7. Run the pipeline: `python src/main.py`

## Learning Milestones
- [ ] Fetch data from CoinGecko API
- [ ] Save raw JSON to `data/raw/`
- [ ] Transform and clean data with pandas
- [ ] Load cleaned data into PostgreSQL
- [ ] Write SQL analysis queries
- [ ] Add logging
- [ ] Add error handling
- [ ] Write basic tests
