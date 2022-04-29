import logging

from typing import Awaitable, Callable

from fastapi import FastAPI

from app.db.mongodb import db, AsyncIOMotorClient
from app.settings import settings

def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.
    This function use fastAPI app to store data,
    such as db_engine.
    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    async def _startup() -> None:
        db.client = AsyncIOMotorClient(settings.mongo_url(),
                                    maxPoolSize=settings.mongo_max_connections_count,
                                    minPoolSize=settings.mongo_min_connections_count)

    return _startup

def shutdown(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.
    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    async def _shutdown() -> None:
        db.client.close()

    return _shutdown
