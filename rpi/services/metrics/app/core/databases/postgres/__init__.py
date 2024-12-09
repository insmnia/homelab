from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.sql.expression import text
from app.core.logging import get_logger
from app.core.settings import get_settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base


settings = get_settings()
postgres_engine = create_async_engine(url=settings.POSTGRES_DSN, echo=False)
AsyncPostgresSession = async_sessionmaker(postgres_engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
logger = get_logger("Postgres")


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgresSession() as _session:
        try:
            yield _session
        except Exception:
            logger.exception("Error on database session")
            await _session.rollback()
            raise
        finally:
            await _session.close()


@asynccontextmanager
async def tx_session_factory() -> AsyncGenerator[AsyncSession, None]:
    """Transactional session"""
    async with AsyncPostgresSession() as _session:
        try:
            async with _session.begin():
                yield _session
                await _session.commit()
        except Exception:
            logger.exception("[TX Session Rollback] Error on database session")
            await _session.rollback()
            raise
        finally:
            await _session.close()


async def check_db() -> bool:
    try:
        async with postgres_engine.connect() as conn:
            await conn.execute(text("SELECT * FROM user"))
        return True
    except Exception as e:
        logger.debug(str(e))
        return False
