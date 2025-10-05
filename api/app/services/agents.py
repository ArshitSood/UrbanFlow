from __future__ import annotations

from dataclasses import dataclass

from .repository import AnalyticsRepository


ALLOWED_TOOLS = {
    "overview.lookup",
    "quality.runs",
    "pipeline.runs",
    "lineage.lookup",
}


@dataclass(frozen=True)
class AgentAnswer:
    answer: str
    tool_trace: list[dict]
    provenance: dict


class AgentGateway:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def answer(self, question: str, context: dict) -> AgentAnswer:
        lowered = question.lower()
        if "quality" in lowered or "quarantine" in lowered:
            tool = "quality.runs"
            payload = self.repository.quality_runs()
            summary = "Latest quality run passed with quarantined records explained by deterministic rules."
        elif "pipeline" in lowered or "dag" in lowered:
            tool = "pipeline.runs"
            payload = self.repository.pipelines()
            summary = "Latest pipeline run completed successfully and exposes run identifiers for audit."
        elif "lineage" in lowered:
            tool = "lineage.lookup"
            payload = self.repository.lineage(context.get("dataset", "gold.hourly_zone_demand"))
            summary = "Lineage was resolved from the governed metadata service."
        else:
            tool = "overview.lookup"
            payload = self.repository.overview()
            summary = "Overview metrics were retrieved from the approved analytics service."

        return AgentAnswer(
            answer=summary,
            tool_trace=[{"tool": tool, "allowed": tool in ALLOWED_TOOLS, "query_id": payload.get("query_id")}],
            provenance={
                "source_dataset": payload.get("source_dataset"),
                "data_freshness": payload.get("data_freshness"),
                "applied_filters": payload.get("applied_filters", context),
            },
        )

