terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name = "urbanflow-${var.environment}"
}

resource "google_storage_bucket" "raw" {
  name                        = "${local.name}-raw"
  location                    = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
  labels = {
    app = "urbanflow"
    env = var.environment
  }
}

resource "google_storage_bucket" "curated" {
  name                        = "${local.name}-curated"
  location                    = var.region
  uniform_bucket_level_access = true
  labels = {
    app = "urbanflow"
    env = var.environment
  }
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id                 = replace(local.name, "-", "_")
  location                   = var.region
  delete_contents_on_destroy = false
  labels = {
    app = "urbanflow"
    env = var.environment
  }
}

resource "google_pubsub_topic" "trip_replay" {
  name = "${local.name}-trip-replay"
  labels = {
    app = "urbanflow"
    env = var.environment
  }
}

resource "google_service_account" "api" {
  account_id   = "${local.name}-api"
  display_name = "UrbanFlow API service account"
}

resource "google_service_account" "pipeline" {
  account_id   = "${local.name}-pipeline"
  display_name = "UrbanFlow pipeline service account"
}
