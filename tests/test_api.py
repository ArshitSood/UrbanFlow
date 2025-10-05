from fastapi.testclient import TestClient

from api.app.main import app


client = TestClient(app)


def test_overview_includes_provenance() -> None:
    response = client.get("/api/v1/overview")
    assert response.status_code == 200
    payload = response.json()
    assert payload["source_dataset"]
    assert payload["data_freshness"]
    assert payload["query_id"]


def test_backfill_is_protected_by_default() -> None:
    response = client.post(
        "/api/v1/operations/backfill",
        json={"service": "yellow", "year": 2026, "month": 1, "confirmation": "BACKFILL yellow 2026-01"},
    )
    assert response.status_code == 403


def test_agent_returns_tool_trace() -> None:
    response = client.post(
        "/api/v1/agents/query",
        json={"agent": "pipeline_ops", "question": "What is the latest pipeline status?", "context": {}},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["tool_trace"][0]["allowed"] is True
    assert payload["provenance"]["source_dataset"]

