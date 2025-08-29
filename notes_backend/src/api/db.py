"""
Database configuration and session management for the Notes API.

This module sets up the SQLAlchemy engine, session factory, and declarative base.
Configuration is read from environment variables using python-dotenv.

Environment variables:
- DATABASE_URL: SQLAlchemy database URL (default: sqlite:///./notes.db)
- DB_ECHO: "true"/"false" to enable SQL echo (default: false)
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Load .env if present (non-fatal if missing)
load_dotenv()

# Read env with safe defaults
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./notes.db")
DB_ECHO: bool = os.getenv("DB_ECHO", "false").lower() in ("1", "true", "yes")

# For SQLite in local files, we need check_same_thread=False for multi-threaded FastAPI
connect_args: Optional[dict] = None
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=DB_ECHO, connect_args=connect_args or {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    """
    Initialize database by creating tables if they do not exist.
    """
    from .models import NoteORM  # noqa: F401 (ensure models are registered)
    Base.metadata.create_all(bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy Session to FastAPI dependencies, closing it after use."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.

    Useful for scripts or background tasks.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
