select
  *,
  extract(hour from pickup_at) as pickup_hour_of_day,
  extract(dayofweek from pickup_at) as pickup_day_of_week,
  case
    when pickup_location_id in (1, 132, 138) or dropoff_location_id in (1, 132, 138)
      then true
    else false
  end as is_airport_trip
from {{ ref('stg_canonical_trips') }}

