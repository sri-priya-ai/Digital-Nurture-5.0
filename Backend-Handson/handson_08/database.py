"""
database.py
Sets up the SQLAlchemy engine, session factory, and declarative Base
used by all models in the Course Management API.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file database - simple and file-based, good for a hands-on exercise
SQLALCHEMY_DATABASE_URL = "sqlite:///./course_management.db"

# check_same_thread=False is needed only for SQLite (FastAPI can use
# the same connection from multiple threads/requests)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and
    guarantees it is closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
