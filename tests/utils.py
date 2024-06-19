# from app.utils.dependencies import uow_dep
# from app.utils.unit_of_work import UnitOfWork
#
# uow_obj = UnitOfWork()
#
#
# async def get_from_db(uow):
#     async with uow:
#         user = await uow.users.select_first_by_kwargs(
#             username="max31ru12"
#         )
#         print(user)
#
#
# import asyncio
#
# asyncio.run(get_from_db(uow_obj))
