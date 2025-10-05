from __future__ import annotations

from datetime import datetime, timezone


GENERATED_AT = datetime.now(timezone.utc).isoformat()


OVERVIEW = {
    "generated_at": GENERATED_AT,
    "source_dataset": "development_fixture:gold.mobility_metrics",
    "data_freshness": {"latest_source_month": "2026-01", "warehouse_published_at": GENERATED_AT},
    "applied_filters": {"service_type": "yellow", "date_range": ["2026-01-01", "2026-01-31"]},
    "query_id": "fixture-overview-001",
    "kpis": {
        "trips_processed": 12450,
        "active_service_types": 2,
        "quality_gate": "pass",
        "pipeline_health": "healthy",
    },
    "trend": [
        {"date": "2026-01-01", "trip_count": 395},
        {"date": "2026-01-02", "trip_count": 418},
        {"date": "2026-01-03", "trip_count": 402},
    ],
}


QUALITY_RUNS = {
    "generated_at": GENERATED_AT,
    "source_dataset": "development_fixture:quality_runs",
    "data_freshness": {"latest_quality_run_at": GENERATED_AT},
    "items": [
        {
            "run_id": "quality-202601-yellow",
            "dataset": "silver.canonical_trips",
            "partition": "service=yellow/year=2026/month=01",
            "checks_passed": 13,
            "warnings": 1,
            "failures": 0,
            "quarantined_records": 7,
            "status": "pass",
        }
    ],
}


PIPELINES = {
    "generated_at": GENERATED_AT,
    "source_dataset": "development_fixture:pipeline_runs",
    "data_freshness": {"latest_run_at": GENERATED_AT},
    "items": [
        {
            "run_id": "run-yellow-2026-01",
            "dag_id": "urbanflow_monthly_partition",
            "state": "success",
            "service": "yellow",
            "partition": "2026-01",
            "duration_seconds": 812,
            "rows_processed": 12450,
            "retries": 1,
        }
    ],
}

