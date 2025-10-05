from __future__ import annotations

from fastapi import APIRouter

from api.app.services.repository import AnalyticsRepository

router = APIRouter(prefix="/api/v1", tags=["analytics"])
repo = AnalyticsRepository()


@router.get("/overview")
def overview() -> dict:
    return repo.overview()


@router.get("/mobility/zones")
def mobility_zones() -> dict:
    data = repo.overview()
    return {**data, "source_dataset": "development_fixture:gold.hourly_zone_demand"}


@router.get("/mobility/routes")
def mobility_routes() -> dict:
    return {"generated_at": repo.overview()["generated_at"], "source_dataset": "development_fixture:gold.route_performance", "items": []}


@router.get("/mobility/airports")
def mobility_airports() -> dict:
    return {"generated_at": repo.overview()["generated_at"], "source_dataset": "development_fixture:gold.airport_metrics", "items": []}


@router.get("/revenue")
def revenue() -> dict:
    return {"generated_at": repo.overview()["generated_at"], "source_dataset": "development_fixture:gold.revenue_metrics", "items": []}


@router.get("/lineage/{dataset}")
def lineage(dataset: str) -> dict:
    return repo.lineage(dataset)

