from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="urbanflow_monthly_partition",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    params={
        "service": Param("yellow", enum=["yellow", "green", "fhvhv"]),
        "year": Param(2026, type="integer"),
        "month": Param(1, type="integer", minimum=1, maximum=12),
    },
    tags=["urbanflow", "mobility", "backfill-safe"],
) as dag:
    discover_source_files = EmptyOperator(task_id="discover_source_files")

    ingest_monthly_partition = BashOperator(
        task_id="ingest_monthly_partition",
        bash_command=(
            "python -m ingestion.urbanflow_ingestion.cli "
            "--service {{ params.service }} --year {{ params.year }} --month {{ params.month }}"
        ),
    )

    validate_bronze = EmptyOperator(task_id="validate_bronze")
    spark_silver_transform = EmptyOperator(task_id="spark_silver_transform")
    quality_gate = EmptyOperator(task_id="quality_gate")
    build_gold = EmptyOperator(task_id="build_gold")
    dbt_test_and_publish = BashOperator(task_id="dbt_test_and_publish", bash_command="dbt build --project-dir dbt")
    refresh_metadata = EmptyOperator(task_id="refresh_metadata")

    (
        discover_source_files
        >> ingest_monthly_partition
        >> validate_bronze
        >> spark_silver_transform
        >> quality_gate
        >> build_gold
        >> dbt_test_and_publish
        >> refresh_metadata
    )

