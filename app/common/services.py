from contextvars import ContextVar
from typing import Any, Self, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

session_context: ContextVar[AsyncSession | None] = ContextVar("session", default=None)


class DBController:

    @property
    def session(self):
        session = session_context.get()
        if session is None:
            raise ValueError("Session is not initialized")
        return session


db: DBController = DBController()


class MappingBase:

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        entity = cls(**kwargs)  # noqa
        db.session.add(entity)
        await db.session.flush()
        await db.session.commit()
        return entity

    @classmethod
    async def get_all(cls) -> Sequence[Self]:
        return (await db.session.execute(select(cls))).scalars().all()

    @classmethod
    async def select_by_kwargs(cls, *order: Any, **kwargs: Any) -> Sequence[Self]:
        stmt = select(cls).filter_by(**kwargs).order_by(*order)
        return (await db.session.execute(stmt)).scalars().all()

    @classmethod
    async def select_first_by_kwargs(cls, *order: Any, **kwargs) -> Self:
        stmt = select(cls).filter_by(**kwargs).order_by(*order)
        return (await db.session.execute(stmt)).scalars().first()

    async def delete(self) -> None:
        await db.session.delete(self)
        await db.session.flush()
        await db.session.commit()

    async def update(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.session.commit()
        return self
