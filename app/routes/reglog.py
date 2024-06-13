from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException
from starlette.status import HTTP_409_CONFLICT

from app.models.users_db import User
from app.utils.dependencies import uow_dep

router = APIRouter(tags=["register"])


@router.post(
    "/register/",
    response_model=User.FullModel,
    status_code=201,
)
async def register(data: User.RegisterModel, uow: uow_dep):
    async with uow:
        user = await uow.users.select_first_by_kwargs(email=data.email)
        if user is not None:
            raise HTTPException(HTTP_409_CONFLICT, detail="Email already in use")
        user = await uow.users.create(**data.model_dump())
        print(user)
        await uow.commit()
    return user


class SignIn(BaseModel):
    username: str
    password: Annotated[str, Field(min_length=4, max_length=100)]
