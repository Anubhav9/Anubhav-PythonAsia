output "gcp_database_host" {
  description = "Private IP address for Cloud SQL Postgres instance"
  value       = google_sql_database_instance.python_asia_postgres.private_ip_address
}

output "gcp_database_username" {
  description = "Cloud SQL database username for decision-service"
  value       = google_sql_user.custom_admin.name
}

output "gcp_database_name" {
  description = "Cloud SQL database name"
  value       = google_sql_database.pythonasiadb.name
}

output "decision_service_gsa_email" {
  description = "GCP service account email used by decision-service via Workload Identity"
  value       = google_service_account.decision_service_gsa.email
}
