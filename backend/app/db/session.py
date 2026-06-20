from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import settings

engine = create_async_engine(settings.db.DATABASE_URL, echo=False)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Get a database session. Does not depend on Litestar config."""
    async with sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
