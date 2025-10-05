from api.app.services.repository import AnalyticsRepository


def test_repository_responses_expose_contract_metadata() -> None:
    repo = AnalyticsRepository()
    for payload in [repo.overview(), repo.quality_runs(), repo.pipelines(), repo.lineage("gold.hourly_zone_demand")]:
        assert payload["generated_at"]
        assert payload["source_dataset"]

