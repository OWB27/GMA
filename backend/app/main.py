from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.modeling_jobs import router as modeling_jobs_router
from app.api.routes.review import router as review_router
from app.api.routes.workflow import router as workflow_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(health_router)
    app.include_router(workflow_router)
    app.include_router(modeling_jobs_router)
    app.include_router(review_router)

    return app


app = create_app()
