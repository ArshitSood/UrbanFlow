from __future__ import annotations

from .fixtures import OVERVIEW, PIPELINES, QUALITY_RUNS


class AnalyticsRepository:
    """Adapter boundary for BigQuery-backed production repositories."""

    def overview(self) -> dict:
        return OVERVIEW

    def quality_runs(self) -> dict:
        return QUALITY_RUNS

    def pipelines(self) -> dict:
        return PIPELINES

    def lineage(self, dataset: str) -> dict:
        return {
            "dataset": dataset,
            "generated_at": OVERVIEW["generated_at"],
            "source_dataset": "development_fixture:lineage",
            "nodes": [
                {"id": "bronze.tlc_tripdata", "layer": "bronze"},
                {"id": "silver.canonical_trips", "layer": "silver"},
                {"id": "gold.hourly_zone_demand", "layer": "gold"},
            ],
            "edges": [
                {"from": "bronze.tlc_tripdata", "to": "silver.canonical_trips"},
                {"from": "silver.canonical_trips", "to": "gold.hourly_zone_demand"},
            ],
        }

