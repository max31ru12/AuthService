from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.common.config import DEV_MODE
from app.routes import reglog
from app.utils.setup import reinit_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    if DEV_MODE:
        await reinit_database()
    yield


app = FastAPI(
    title="Test FastAPI project",
    lifespan=lifespan,
)

app.include_router(reglog.router, prefix="/api/v1")
