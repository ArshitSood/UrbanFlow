output "raw_bucket" {
  value = google_storage_bucket.raw.name
}

output "curated_bucket" {
  value = google_storage_bucket.curated.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.warehouse.dataset_id
}

output "trip_replay_topic" {
  value = google_pubsub_topic.trip_replay.name
}

