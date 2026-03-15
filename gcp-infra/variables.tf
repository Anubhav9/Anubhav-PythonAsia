variable "python_asia_nomenclature" {
  type        = string
  description = "Nomenclature to be used for Python Asia Components"
  default     = "python-asia"
}

variable "python_asia_gcp_project_id" {
  type        = string
  description = "GCP project id for Python Asia infrastructure"
  default     = "pythonasia-v1"
}

variable "python_asia_region" {
  type        = string
  description = "Primary GCP region"
  default     = "asia-northeast2"
}

variable "python_asia_subnet_range" {
  type        = string
  description = "Subnet IPV4 CIDR Block"
  default     = "10.0.4.0/22"
}

variable "python_asia_gcs_bucket" {
  type        = string
  description = "Globally unique name for the GCS Bucket"
  default     = "approval-letters-python-asia-2026-demo"
}

variable "python_asia_gcs_bucket_location" {
  type        = string
  description = "Region for GCS Bucket for Python Asia"
  default     = "ASIA-NORTHEAST2"
}

variable "python_asia_db_password" {
  type        = string
  description = "Cloud SQL password for custom_admin"
  sensitive   = true
}
