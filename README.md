# UrbanFlow

Scalable Urban Mobility Data Platform for official NYC TLC trip-record data.

UrbanFlow is a production-style data engineering portfolio project. It ingests monthly TLC Parquet files into immutable Bronze storage, validates and normalizes records into Silver, publishes analytics-ready Gold models, exposes operational metadata through FastAPI, and presents analytics, quality, lineage, and pipeline health in a React dashboard. A constrained agent layer can answer questions only through approved backend tools.

## Architecture

```text
NYC TLC Parquet
  -> GCS Bronze
  -> PySpark / Dataproc
  -> Silver canonical trips + invalid quarantine
  -> Gold analytical products
  -> BigQuery + dbt
  -> FastAPI
  -> React dashboard + Agent Tool Gateway
```

## What Is Included

- Manifest-driven ingestion with idempotent destination naming and checksum metadata.
- PySpark Bronze to Silver transform with deterministic validation and quarantine reasons.
- PySpark Silver to Gold builders for hourly demand, route performance, airport metrics, revenue metrics, and mobility metrics.
- Airflow DAG parameterized by service, year, and month.
- dbt staging, intermediate, and mart models with tests and documented grain.
- FastAPI service with versioned analytics, quality, pipeline, lineage, and agent endpoints.
- React + TypeScript dashboard source with an enterprise data-product layout and contextual agent drawer.
- Terraform for GCS, BigQuery, Pub/Sub, service accounts, and deployment variables.
- Tests, golden fixtures, performance benchmark stubs, CI workflow, and documentation.

## Local Development

The local path uses committed fixtures and adapter interfaces. It is intentionally separate from production mode and should not be used for resume metrics.

```bash
cd urbanflow_advanced
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
uvicorn api.app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Cloud Deployment Path

1. Configure a GCP project and workload identity.
2. Copy `.env.example` to `.env` for non-secret configuration.
3. Run `terraform init` and `terraform plan` from `terraform/`.
4. Build API and Spark containers through CI.
5. Use the Airflow DAG to ingest a real TLC month end to end.
6. Run dbt tests before publishing downstream marts.

## Ground Rules

- Bronze data is immutable.
- Reruns are idempotent and backfill-safe.
- Quality failures are deterministic and retain provenance.
- Dashboard values come from API/model contracts, not hard-coded UI constants.
- Agents are read-only by default and must expose source, filters, freshness, and tool trace.
- Resume metrics must come from `docs/benchmark.md` after running reproducible benchmarks.

