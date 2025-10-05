# Data Contracts

## Silver Canonical Trips

Grain: one validated source trip record.

Required fields:

- `service_type`
- `pickup_at`
- `dropoff_at`
- `trip_date`
- `pickup_location_id`
- `dropoff_location_id`
- `_source_file`
- `_ingestion_id`

Invalid rows are not dropped silently. They are written to quarantine with `rejection_code`, `rejection_reason`, ingestion metadata, and original source reference.

## Gold Hourly Zone Demand

Grain: one pickup zone, service type, and pickup hour.

Partition: `trip_date`

Cluster candidates: `service_type`, `pickup_location_id`

