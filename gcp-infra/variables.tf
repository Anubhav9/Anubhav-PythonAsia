variable "python_asia_nomenclature" {
  type = string
  description = "Nomenclature to be used for Python Asia Components"
  default = "python-asia"
}

variable "python_asia_subnet_range" {
  type = string
  description = "Subnet IPV4 CIDR Block"
  default = "10.0.4.0/22"
}

variable "python_asia_gcs_bucket" {
  type = string
  description = "Globally unique name for the GCS Bucket"
  default = "approval-letters-python-asia"
}

variable "python_asia_gcs_bucket_location" {
  type = string
  description = "Region for GCS Bucket for Python Asia"
  default = "ASIA-NORTHEAST2"
}
