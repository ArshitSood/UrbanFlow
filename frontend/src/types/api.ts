export type Freshness = {
  latest_source_month?: string;
  warehouse_published_at?: string;
  latest_run_at?: string;
};

export type OverviewResponse = {
  generated_at: string;
  source_dataset: string;
  data_freshness: Freshness;
  applied_filters: Record<string, unknown>;
  query_id: string;
  kpis: {
    trips_processed: number;
    active_service_types: number;
    quality_gate: string;
    pipeline_health: string;
  };
  trend: Array<{ date: string; trip_count: number }>;
};

export type PipelineRun = {
  run_id: string;
  dag_id: string;
  state: string;
  service: string;
  partition: string;
  duration_seconds: number;
  rows_processed: number;
  retries: number;
};

export type QualityRun = {
  run_id: string;
  dataset: string;
  partition: string;
  checks_passed: number;
  warnings: number;
  failures: number;
  quarantined_records: number;
  status: string;
};

