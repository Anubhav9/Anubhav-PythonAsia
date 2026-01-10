resource "google_compute_network" "python_asia_vpc" {
  name = "${var.python_asia_nomenclature}-vpc"
  auto_create_subnetworks = false
}