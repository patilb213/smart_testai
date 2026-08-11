import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DB_DIR, "app.db")

os.makedirs(DB_DIR, exist_ok=True)

class Config:
    # Falls back to a guaranteed-correct absolute SQLite path if DATABASE_URL
    # isn't set in .env. When migrating to MongoDB/Postgres later, just add
    # DATABASE_URL to .env with the real connection string — no code changes needed.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-this")