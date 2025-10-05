from pathlib import Path

from ingestion.urbanflow_ingestion.manifest import build_manifest


def test_manifest_is_idempotent_for_same_source_file(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.parquet"
    file_path.write_bytes(b"fixture")

    first = build_manifest(
        service="yellow",
        year=2026,
        month=1,
        source_url="https://example.test/yellow.parquet",
        local_file=file_path,
        raw_bucket="urbanflow-raw",
        schema_version="yellow-v1",
    )
    second = build_manifest(
        service="yellow",
        year=2026,
        month=1,
        source_url="https://example.test/yellow.parquet",
        local_file=file_path,
        raw_bucket="urbanflow-raw",
        schema_version="yellow-v1",
    )

    assert first.ingestion_id == second.ingestion_id
    assert first.bronze_object_path == second.bronze_object_path

