from pathlib import Path  # ✅ add this
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Paths
BASE_DIR = Path(__file__).resolve().parent              # .../backend
DATA_DIR = (BASE_DIR / "data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "database.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine / Session / Base
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + FastAPI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
