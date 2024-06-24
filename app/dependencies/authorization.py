from typing import Annotated, Final

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie, APIKeyHeader
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.session_db import Session
from app.models.users_db import User

AUTH_COOKIE: Final = "auth_cookie"
AUTH_HEADER: Final = "auth_header"

auth_cookie = APIKeyCookie(name=AUTH_COOKIE, scheme_name="auth cookie", auto_error=False)
auth_header = APIKeyHeader(name=AUTH_HEADER, scheme_name="auth header", auto_error=False)

AuthCookie = Annotated[str | None, Depends(auth_cookie)]
AuthHeader = Annotated[str | None, Depends(auth_header)]


def add_session_to_response(
        response: Response,
        session: Session
) -> None:
    response.set_cookie(
        key=AUTH_COOKIE,
        value=session.token,
    )


def remove_session_from_response(
        response: Response
) -> None:
    response.delete_cookie(key=AUTH_COOKIE)


async def authorized_session(
        cookie_token: AuthCookie,
        header_token: AuthHeader,
) -> Session:
    token = cookie_token or header_token
    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    session = await Session.select_first_by_kwargs(token=token)
    if session is None or session.expired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )
    return session


AuthorizedSession = Annotated[Session, Depends(authorized_session)]


async def authorize_user(
        session: AuthorizedSession,
) -> User:
    return await User.select_first_by_kwargs(id=session.user_id)


AuthorizedUser = Annotated[User, Depends(authorize_user)]
