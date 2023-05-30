import os

from dotenv import load_dotenv

load_dotenv()

DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = (f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
                f"/{DB_NAME}")


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MAX_DISTANCE_TO_CARGO = 450

AUTO_LOCATION_REFRESH_RATE = 180  # seconds
