from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

WORKDIR: Path = Path.cwd()

load_dotenv(WORKDIR / ".env")

DEV_MODE: bool = getenv("DEV_MODE", default="1") == "1"

DB_URL = getenv("DB_URL", default="postgresql+asyncpg://test:test@localhost:5432/test")

async_engine: AsyncEngine = create_async_engine(
    url=DB_URL,
    echo=DEV_MODE,
    pool_size=5,
)

sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False)

db_meta = MetaData()


class Base(DeclarativeBase):
    metadata = db_meta

    def __repr__(self):
        cols = [
            f"{col} = {getattr(self, col)}" for col in self.__table__.columns.keys()
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
