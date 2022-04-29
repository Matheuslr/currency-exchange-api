import time
from typing import Awaitable, Callable

from fastapi import FastAPI


def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.
    This function use fastAPI app to store data,
    such as db_engine.
    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    async def _startup() -> None:
        pass

        # Instrumentation and Log correlation


def shutdown(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.
    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    async def _shutdown() -> None:
        pass

    return _shutdown
