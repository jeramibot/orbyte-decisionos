import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from backend.models.entities import Base

ROOT = Path(__file__).resolve().parents[1]


def make_engine(url=None):
    (ROOT / "data/runtime").mkdir(parents=True, exist_ok=True)
    url = url or os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'data/runtime/decisionos.db'}")
    engine = create_engine(url, connect_args={"check_same_thread": False, "timeout": 15} if url.startswith("sqlite") else {})
    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def sqlite_settings(conn, _):
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA journal_mode=WAL")
    return engine


def session_factory(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(engine, expire_on_commit=False)
