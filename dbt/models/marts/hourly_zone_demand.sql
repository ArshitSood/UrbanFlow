select
  trip_date,
  timestamp_trunc(pickup_at, hour) as pickup_hour,
  service_type,
  pickup_location_id,
  count(*) as trip_count,
  sum(passenger_count) as passenger_count,
  avg(trip_duration_minutes) as avg_duration_minutes
from {{ ref('int_trip_metrics') }}
group by 1, 2, 3, 4

