import asyncio
import logging
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import db_config

logger = logging.getLogger(__name__)

DATABASE_URL = db_config.db.DATABASE_URL

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 1.0

engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    last_exception = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            async with AsyncSessionLocal() as session:
                yield session
                await session.commit()
            return
        except Exception as exc:
            last_exception = exc
            logger.warning("DB attempt %d/%d failed: %s", attempt, _MAX_RETRIES, exc)
            if attempt < _MAX_RETRIES:
                await asyncio.sleep(_RETRY_DELAY_SECONDS * attempt)
    if last_exception:
        raise last_exception


async def init_db():
    async with engine.begin() as conn:
        from src.services.models import SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created / verified.")


async def close_db():
    await engine.dispose()
    logger.info("Database engine disposed.")
