from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_application()
