from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.library import router
from app.core.config import ALLOWED_ORIGINS
from app.services.library import library_service


def create_app() -> FastAPI:
    app = FastAPI(title="CPA-ZH Knowledge API", version="1.0.0", docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.add_middleware(CORSMiddleware, allow_origins=list(ALLOWED_ORIGINS), allow_credentials=False, allow_methods=["GET"], allow_headers=["Accept", "Content-Type"])
    app.include_router(router, prefix="/api/v1")

    @app.on_event("startup")
    def build_indexes() -> None:
        library_service.build_backlinks()

    return app


app = create_app()
