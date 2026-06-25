# database.py — Database connection setup using SQLAlchemy.
# get_db() is a dependency injected into each endpoint that needs
# database access — FastAPI calls it automatically before the handler runs.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./courses.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Yields a database session per request and closes it after.
    Used as a FastAPI Dependency: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
