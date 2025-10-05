# Agent Tool Catalog

Agents may call only these backend-owned tools:

- `overview.lookup`: retrieves approved overview metrics and freshness.
- `quality.runs`: retrieves deterministic quality check outcomes and quarantine counts.
- `pipeline.runs`: retrieves Airflow/Composer run status and task metadata.
- `lineage.lookup`: retrieves governed dataset dependencies.

Browser-provided SQL is not a tool. Operational mutations require RBAC, confirmation, and environment enablement.

