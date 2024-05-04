from typing import Annotated, Final
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import APIKeyCookie
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from app.models.users_db import User
from app.models.session_db import Session


AUTH_COOKIE_NAME: Final[str] = "session"

cookie_auth_scheme = APIKeyCookie(name=AUTH_COOKIE_NAME, auto_error=False)

AuthCookie = Annotated[str | None, Depends(cookie_auth_scheme)]


async def set_session_cookie(response: Response, user: User) -> None:
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=(await Session.create(user=user,user_id=user.id,)).token
    )


async def delete_session_cookie(request: Request, response: Response) -> None:

    session = await Session.select_first_by_kwargs(
        token=request.cookies[AUTH_COOKIE_NAME]
    )
    if session is None:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="Already unauthorized"
        )
    session.disable()
    response.delete_cookie(AUTH_COOKIE_NAME)


async def authorize_session(
    cookie_token: AuthCookie = None
) -> Session:
    if cookie_token is None:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="Authorization is missing"
        )
    session = await Session.select_first_by_kwargs(token=cookie_token)
    if session is None:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="Session is invalid"
        )

    if session.session_expired or not session.status:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    return session


async def authorize_user(
    session: Session = Depends(authorize_session)
) -> User:
    user = await User.select_first_by_kwargs(id=session.user_id)
    if user is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


authorized_session = Annotated[Session, Depends(authorize_session)]
authorized_user = Annotated[User, Depends(authorize_user)]
