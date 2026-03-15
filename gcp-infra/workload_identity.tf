resource "google_service_account" "decision_service_gsa" {
  account_id   = "decision-service-gsa"
  display_name = "Decision service GSA"
}

resource "google_service_account_iam_member" "decision_service_wi_binding" {
  service_account_id = google_service_account.decision_service_gsa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.python_asia_gcp_project_id}.svc.id.goog[default/sa-decision-service]"
}

resource "google_storage_bucket_iam_member" "decision_service_gcs_object_viewer" {
  bucket = google_storage_bucket.python-asia-gcs.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.decision_service_gsa.email}"
}

resource "google_storage_bucket_iam_member" "decision_service_gcs_object_creator" {
  bucket = google_storage_bucket.python-asia-gcs.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.decision_service_gsa.email}"
}
