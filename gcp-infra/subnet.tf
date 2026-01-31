resource "google_compute_subnetwork" "python_asia_subnet" {
  name = "${var.python_asia_nomenclature}-subnet"
  ip_cidr_range = var.python_asia_subnet_range
  network = google_compute_network.python_asia_vpc.id
}