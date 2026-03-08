resource "google_project_service" "sqladmin_api" {
  project            = var.python_asia_gcp_project_id
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "servicenetworking_api" {
  project            = var.python_asia_gcp_project_id
  service            = "servicenetworking.googleapis.com"
  disable_on_destroy = false
}

resource "google_compute_global_address" "private_ip_alloc" {
  name          = "${var.python_asia_nomenclature}-private-ip-alloc"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.python_asia_vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.python_asia_vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
  depends_on              = [google_project_service.servicenetworking_api]
}

resource "google_sql_database_instance" "python_asia_postgres" {
  name             = "decision-service-db"
  database_version = "POSTGRES_16"
  region           = var.python_asia_region

  deletion_protection = false

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.python_asia_vpc.id
    }
  }

  depends_on = [
    google_project_service.sqladmin_api,
    google_service_networking_connection.private_vpc_connection
  ]
}

resource "google_sql_database" "pythonasiadb" {
  name     = "pythonasiadb"
  instance = google_sql_database_instance.python_asia_postgres.name
}

resource "google_sql_user" "custom_admin" {
  name     = "custom_admin"
  instance = google_sql_database_instance.python_asia_postgres.name
  password = var.python_asia_db_password
}
