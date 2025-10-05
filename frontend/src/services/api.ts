import type { OverviewResponse, PipelineRun, QualityRun } from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function fetchOverview() {
  return getJson<OverviewResponse>("/api/v1/overview");
}

export async function fetchPipelines() {
  const payload = await getJson<{ items: PipelineRun[] }>("/api/v1/pipelines");
  return payload.items;
}

export async function fetchQualityRuns() {
  const payload = await getJson<{ items: QualityRun[] }>("/api/v1/data-quality/runs");
  return payload.items;
}

export async function askAgent(question: string, context: Record<string, unknown>) {
  const response = await fetch(`${API_BASE}/api/v1/agents/query`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ agent: "analytics", question, context }),
  });
  if (!response.ok) {
    throw new Error(`Agent request failed: ${response.status}`);
  }
  return response.json();
}

