from __future__ import annotations

from dataclasses import dataclass

from .manifest import ServiceType


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


@dataclass(frozen=True)
class TlcSource:
    service: ServiceType
    year: int
    month: int
    url: str


def monthly_tlc_url(service: ServiceType, year: int, month: int) -> TlcSource:
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    source_name = "fhvhv_tripdata" if service == "fhvhv" else f"{service}_tripdata"
    return TlcSource(
        service=service,
        year=year,
        month=month,
        url=f"{BASE_URL}/{source_name}_{year}-{month:02d}.parquet",
    )

