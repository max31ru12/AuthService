from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **kwargs):
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return (await self.session.execute(stmt)).scalar_one()

    async def delete(self, **kwargs) -> None:
        stmt = delete(self.model).filter_by(**kwargs)
        await self.session.execute(stmt)

    async def find_all(self):
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars().all()

    async def select_by_kwargs(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        return (await self.session.execute(stmt)).scalars().all()

    async def select_first_by_kwargs(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        return (await self.session.execute(stmt)).scalars().first()
