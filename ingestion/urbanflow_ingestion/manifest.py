from __future__ import annotations

import hashlib
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


ServiceType = Literal["yellow", "green", "fhvhv"]
IngestionStatus = Literal["discovered", "downloaded", "validated", "promoted", "failed"]


@dataclass(frozen=True)
class IngestionManifest:
    ingestion_id: str
    service: ServiceType
    year: int
    month: int
    source_url: str
    file_type: str
    checksum_sha256: str
    bronze_object_path: str
    schema_version: str
    status: IngestionStatus
    ingested_at: str
    row_count: int | None = None
    failure_reason: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def bronze_object_path(bucket: str, service: ServiceType, year: int, month: int, checksum: str) -> str:
    return (
        f"gs://{bucket}/bronze/{service}/year={year}/month={month:02d}/"
        f"{service}_{year}_{month:02d}_{checksum[:12]}.parquet"
    )


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_manifest(
    *,
    service: ServiceType,
    year: int,
    month: int,
    source_url: str,
    local_file: Path,
    raw_bucket: str,
    schema_version: str,
    status: IngestionStatus = "downloaded",
    row_count: int | None = None,
) -> IngestionManifest:
    checksum = sha256_file(local_file)
    return IngestionManifest(
        ingestion_id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{service}:{year}:{month}:{checksum}")),
        service=service,
        year=year,
        month=month,
        source_url=source_url,
        file_type="parquet",
        checksum_sha256=checksum,
        bronze_object_path=bronze_object_path(raw_bucket, service, year, month, checksum),
        schema_version=schema_version,
        status=status,
        ingested_at=datetime.now(timezone.utc).isoformat(),
        row_count=row_count,
    )

