# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import AsyncSession
#
# pytestmark = pytest.mark.anyio
#
#
# async def test_register(
#     client: TestClient,
#     session: AsyncSession,
# ):
#     user_data = {
#         "username": "max31ru12",
#         "email": "data1",
#         "password": "data1",
#     }
#
#     response = client.post(
#         url='/register/',
#         json=user_data,
#     )
#
#     # async with uow as uow:
#     #     user = await uow.users.select_first_by_kwargs(username="max31ru12")
#
#     assert response.status_code == 201
#
#
# async def test_register_no_data(
#         client: TestClient,
# ) -> None:
#     response = client.post(
#         url='/register/',
#         json={},
#     )
#
#     assert response.status_code == 422
