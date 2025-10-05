select
  service_type,
  pickup_at,
  dropoff_at,
  trip_date,
  pickup_location_id,
  dropoff_location_id,
  passenger_count,
  trip_distance_miles,
  trip_duration_minutes,
  average_speed_mph,
  fare_amount,
  tip_amount,
  tolls_amount,
  total_amount,
  _source_file,
  _ingestion_id,
  _ingested_at,
  _schema_version
from {{ source('silver', 'canonical_trips') }}

