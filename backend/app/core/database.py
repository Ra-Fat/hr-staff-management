import asyncio
import logging

import asyncpg
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

_engine = None
_session_factory = None


async def init_db(database_url: str) -> None:
    """Connect to the database. Schema migrations are handled by Alembic, not here."""
    global _engine, _session_factory
    retries = 5
    while retries > 0:
        try:
            _engine = create_async_engine(
                database_url,
                echo=False,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
            _session_factory = async_sessionmaker(
                _engine, class_=AsyncSession, expire_on_commit=False
            )
            # Verify connectivity
            async with _engine.connect():
                pass
            logger.info("Database connection established.")
            return
        except (exc.OperationalError, asyncpg.CannotConnectNowError) as e:
            retries -= 1
            logger.warning("DB connection failed, retrying... (%d left) — %s", retries, e)
            await asyncio.sleep(5)
    raise RuntimeError("Could not connect to the database after retries.")


async def close_db() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
    logger.info("Database connection closed.")


async def get_db():
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() during app startup.")
    async with _session_factory() as session:
        yield session
