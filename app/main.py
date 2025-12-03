from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    # Show interactive docs in non-production environments only
    show_docs = settings.APP_ENV != "production"

    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        docs_url="/docs" if show_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if show_docs else None,
    )

    # Mount versioned API
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_application()
