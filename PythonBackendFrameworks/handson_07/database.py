from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = 'sqlite+aiosqlite:///./courses.db'

async_eng = create_async_engine(DB_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=async_eng,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as sess:
        yield sess
