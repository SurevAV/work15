from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .user import User
from .promt import Promt
from .consultant import Consultant
from .commentator import Commentator
from .base import Base
from data import Config


async def setup():

    engine = create_async_engine(
        f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_sessionmaker
