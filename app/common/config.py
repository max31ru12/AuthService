from dotenv import load_dotenv
from pathlib import Path
from os import getenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

from app.common.services import MappingBase

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


class Base(DeclarativeBase, MappingBase):
    metadata = db_meta

    def __repr__(self):
        cols = [f"{col} = {getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
