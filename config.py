import os
from dotenv import load_dotenv

load_dotenv()

# CSV files
TITLES_FILE = "data/titles.csv"
CREDITS_FILE = "data/credits.csv"

# MySQL configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_NAME = os.getenv("DB_NAME", "netflix_analytics")