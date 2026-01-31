resource "google_storage_bucket" "python-asia-gcs" {
  name = var.python_asia_gcs_bucket
  location = var.python_asia_gcs_bucket_location
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  labels = {
    project = "${var.python_asia_nomenclature}-project"
    owner   = "Anubhav Sanyal"
    env     = "dev"
  }
}
