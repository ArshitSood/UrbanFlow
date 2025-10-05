# Architecture

UrbanFlow separates ingestion, transformation, warehouse modeling, product APIs, and user experience.

## Data Layers

Bronze stores immutable source-aligned Parquet files with source metadata. Silver normalizes service-specific columns into a canonical trip contract and separates invalid rows into quarantine with rejection codes. Gold creates purpose-built aggregate products for zone demand, route performance, airport analysis, revenue, and citywide mobility.

## Trust Model

All dashboard and agent answers are backed by deterministic APIs. Agents do not invent metrics or run arbitrary SQL from the browser. API responses include freshness, filters, source dataset, and query/run identifiers where available.

## Deployment

Terraform provisions GCS, BigQuery, Pub/Sub, and service accounts. Airflow orchestrates monthly partitions and backfills. Dataproc or serverless Spark runs transforms. dbt publishes warehouse models after tests pass.

