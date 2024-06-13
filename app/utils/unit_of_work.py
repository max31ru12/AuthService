from app.common.config import sessionmaker
from app.services.repositories import SessionRepo, UserRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.session_factory = sessionmaker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepo(self.session)
        self.auth_session = SessionRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
