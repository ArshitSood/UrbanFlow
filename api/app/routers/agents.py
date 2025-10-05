from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.app.services.agents import AgentGateway
from api.app.services.repository import AnalyticsRepository

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])
gateway = AgentGateway(AnalyticsRepository())


class AgentQuery(BaseModel):
    agent: str = Field(pattern="^(analytics|data_quality|pipeline_ops|cost_performance)$")
    question: str = Field(min_length=3, max_length=1000)
    context: dict = Field(default_factory=dict)


@router.post("/query")
def query_agent(payload: AgentQuery) -> dict:
    result = gateway.answer(payload.question, payload.context)
    return {
        "agent": payload.agent,
        "answer": result.answer,
        "tool_trace": result.tool_trace,
        "provenance": result.provenance,
    }

