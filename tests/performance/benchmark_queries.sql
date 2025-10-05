-- Run with BigQuery job statistics captured in docs/benchmark.md.
select
  trip_date,
  service_type,
  sum(trip_count) as trips
from `PROJECT.DATASET.hourly_zone_demand`
where trip_date between date('2026-01-01') and date('2026-01-31')
group by 1, 2;

