resource "google_compute_router" "python_asia_router" {
  name    = "${var.python_asia_nomenclature}-router"
  region  = var.python_asia_region
  network = google_compute_network.python_asia_vpc.id
}

resource "google_compute_router_nat" "nat-gateway" {
  name                               = "${var.python_asia_nomenclature}-nat"
  router                             = google_compute_router.python_asia_router.name
  region                             = var.python_asia_region
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  nat_ip_allocate_option             = "AUTO_ONLY"
}
