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
