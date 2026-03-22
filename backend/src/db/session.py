import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    DATABASE_URL = os.environ["DATABASE_URL"]
except Exception:
    raise ValueError("Expected DATABASE_URL to be set")


engine = create_engine(
    DATABASE_URL,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
