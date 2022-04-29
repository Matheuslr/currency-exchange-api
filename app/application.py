from importlib import metadata
from pathlib import Path

from ddtrace import config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.lifetime import shutdown, startup
from app.api.router import api_router
from app.settings import settings

APP_ROOT = Path(__file__).parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    # Override service name
    config.fastapi["service_name"] = str(settings.service_name)

    app = FastAPI(
        title="app",
        description="Fastapi for SBF Challenge",
        # version=metadata.version("app"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
    )
    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router)
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )
    return app
