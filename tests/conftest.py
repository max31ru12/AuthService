from contextlib import asynccontextmanager, AbstractAsyncContextManager

import pytest
from typing import Iterator, AsyncIterator, Protocol
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


from app.main import app
from app.common.config import sessionmaker
from app.common.services import session_context


pytest_plugins = ("anyio", )


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


class ActiveSession(Protocol):
    def __call__(self) -> AbstractAsyncContextManager[AsyncSession]:
        pass


@pytest.fixture()
def active_session() -> ActiveSession:
    @asynccontextmanager
    async def active_session_inner() -> AsyncIterator[AsyncSession]:
        async with sessionmaker.begin() as session:
            session_context.set(session)
            yield session

    return active_session_inner


