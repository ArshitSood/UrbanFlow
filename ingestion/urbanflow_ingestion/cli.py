from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import build_manifest
from .tlc_sources import monthly_tlc_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an UrbanFlow ingestion manifest.")
    parser.add_argument("--service", required=True, choices=["yellow", "green", "fhvhv"])
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--month", required=True, type=int)
    parser.add_argument("--raw-bucket", default="urbanflow-raw-dev")
    parser.add_argument("--schema-version", default="v1")
    parser.add_argument("--local-file", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = monthly_tlc_url(args.service, args.year, args.month)
    local_file = args.local_file or Path(f"/tmp/{args.service}_{args.year}_{args.month:02d}.parquet")
    if not local_file.exists():
        raise FileNotFoundError(
            f"{local_file} does not exist. Download the TLC Parquet file first or pass --local-file."
        )
    manifest = build_manifest(
        service=args.service,
        year=args.year,
        month=args.month,
        source_url=source.url,
        local_file=local_file,
        raw_bucket=args.raw_bucket,
        schema_version=args.schema_version,
    )
    print(json.dumps(manifest.to_dict(), indent=2))


if __name__ == "__main__":
    main()

