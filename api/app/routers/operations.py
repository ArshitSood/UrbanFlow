from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.app.core.config import settings
from api.app.services.repository import AnalyticsRepository

router = APIRouter(prefix="/api/v1", tags=["operations"])
repo = AnalyticsRepository()


class BackfillRequest(BaseModel):
    service: str
    year: int
    month: int
    confirmation: str


@router.get("/data-quality/runs")
def quality_runs() -> dict:
    return repo.quality_runs()


@router.get("/pipelines")
def pipelines() -> dict:
    return repo.pipelines()


@router.get("/pipelines/{run_id}")
def pipeline_run(run_id: str) -> dict:
    runs = repo.pipelines()["items"]
    match = next((run for run in runs if run["run_id"] == run_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="pipeline run not found")
    return {**match, "tasks": [{"task_id": "quality_gate", "state": "success", "duration_seconds": 42}]}


@router.post("/operations/backfill")
def request_backfill(payload: BackfillRequest) -> dict:
    if not settings.agent_write_actions_enabled:
        raise HTTPException(status_code=403, detail="backfill writes are disabled in this environment")
    if payload.confirmation != f"BACKFILL {payload.service} {payload.year}-{payload.month:02d}":
        raise HTTPException(status_code=400, detail="explicit confirmation text is required")
    return {"status": "accepted", "service": payload.service, "year": payload.year, "month": payload.month}

