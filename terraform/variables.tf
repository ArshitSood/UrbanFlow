variable "project_id" {
  type        = string
  description = "GCP project that hosts UrbanFlow."
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Primary deployment region."
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment name used in resource labels."
}

