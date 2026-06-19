from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import db_config

# Database url
DATABASE_URL = db_config.db.DATABASE_URL

engine = create_async_engine(
    url=DATABASE_URL,
    pool_pre_ping=True
)
AsyncSessionLocal = sessionmaker(bind=engine, echo=True, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session