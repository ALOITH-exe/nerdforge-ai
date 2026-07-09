# backend/app/database/__init__.py
from .models import Base, Scenario, Attack, Event, Detection, IOC, Report
from .session import engine, SessionLocal, get_db

def init_db():
    Base.metadata.create_all(bind=engine)

__all__ = [
    "Base", "Scenario", "Attack", "Event", "Detection", "IOC", "Report",
    "engine", "SessionLocal", "get_db", "init_db"
]