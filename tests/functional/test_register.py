import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users_db import User

pytestmark = pytest.mark.anyio


async def test_register(
    client: TestClient,
):
    response = client.post(
        url='/register/',
        json={
            "username": "data",
            "email": "data",
            "password": "data",
        }
    )

    assert response.status_code == 201


async def test_signup(
    active_session: AsyncSession,
):
    async with active_session():  # noqa
        user = await User.create(username="max", email="email@mial.ru", password="asdasdasd")

    assert 1 == 1
