from collections.abc import Sequence
from contextvars import ContextVar
from typing import Any, Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

session_context: ContextVar[AsyncSession | None] = ContextVar("session", default=None)


class DBContorller:
    @property
    def session(self) -> AsyncSession:
        session = session_context.get()
        if session is None:
            raise ValueError("Session not initialized")
        return session


db = DBContorller()


class BaseRepository:

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        entry = cls(**kwargs)  # noqa
        db.session.add(entry)
        await db.session.flush()
        return entry

    @classmethod
    async def select_all(cls):
        stmt = select(cls)
        return (await db.session.execute(stmt)).scalars().all()

    @classmethod
    async def select_first_by_kwargs(cls, **kwargs: Any) -> Self | None:
        stmt = select(cls).filter_by(**kwargs)
        return (await db.session.execute(stmt)).scalars().first()
