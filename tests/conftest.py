# import pytest
# from typing import Iterator
#
# from fastapi import Depends
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
#
# from app.main import app
# from app.common.config import sessionmaker, db_meta, Base
# from app.utils.unit_of_work import UnitOfWork
#
# pytest_plugins = ("anyio",)
#
#
# TEST_DB_URL = "postgresql+asyncpg://test:test@localhost:5432/test"
#
# engine = create_async_engine(
#     TEST_DB_URL,
#     echo=True,
# )
#
# TestingSessionLocal = async_sessionmaker(
#     engine,
# )
#
# # Base.metadata.create_all()
#
#
# @pytest.fixture(scope="session")
# def anyio_backend() -> str:
#     return "asyncio"
#
#
# @pytest.fixture(scope="session")
# def client() -> Iterator[TestClient]:
#     with TestClient(app, base_url="http://localhost/api/v1/") as client:
#         yield client
#
#
# @pytest.fixture(scope="session")
# async def session() -> AsyncSession:
#     yield sessionmaker()
#
