# backend/app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from ..config import settings

# Database URL - normalized so Railway's "postgres://" scheme works with
# SQLAlchemy 2.0 (which requires "postgresql://").
DATABASE_URL = settings.normalized_database_url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,  # avoids stale-connection errors on managed Postgres
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()