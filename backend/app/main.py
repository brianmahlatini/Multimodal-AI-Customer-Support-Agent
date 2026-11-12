from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, cases, health, tickets
from app.core.config import settings
from app.db.session import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Multimodal support automation with agentic triage, ticketing, and human handover.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(cases.router, prefix="/cases", tags=["cases"])
    app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
    app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
    return app


app = create_app()
