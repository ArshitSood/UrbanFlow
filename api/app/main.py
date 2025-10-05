from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app.core.config import settings
from api.app.routers import agents, analytics, operations

app = FastAPI(title="UrbanFlow API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics.router)
app.include_router(operations.router)
app.include_router(agents.router)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
