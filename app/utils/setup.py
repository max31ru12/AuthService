from app.common.config import async_engine, Base
from app.models.users_db import User
from app.models.session_db import Session


async def reinit_database() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
