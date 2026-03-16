resource "google_container_cluster" "python_asia_cluster" {
  name                     = "${var.python_asia_nomenclature}-cluster"
  network                  = google_compute_network.python_asia_vpc.id
  subnetwork               = google_compute_subnetwork.python_asia_subnet.id
  remove_default_node_pool = true
  initial_node_count       = 1

  workload_identity_config {
    workload_pool = "${var.python_asia_gcp_project_id}.svc.id.goog"
  }

}

resource "google_container_node_pool" "public_node" {
  name           = "${var.python_asia_nomenclature}-public-node"
  location       = var.python_asia_region
  cluster        = google_container_cluster.python_asia_cluster.id
  node_count     = 1
  node_locations = ["${var.python_asia_region}-c"]

  node_config {
    preemptible  = false
    machine_type = "e2-medium"
    labels = {
      env       = "dev"
      node-type = "public"
    }
  }

  depends_on = [google_compute_router_nat.nat-gateway]
}

resource "google_container_node_pool" "private_node" {
  name           = "${var.python_asia_nomenclature}-private-node"
  location       = var.python_asia_region
  cluster        = google_container_cluster.python_asia_cluster.id
  node_count     = 1
  node_locations = ["${var.python_asia_region}-c"]

  node_config {
    preemptible  = false
    machine_type = "e2-medium"
    labels = {
      env       = "dev"
      node-type = "private"
    }
  }

  network_config {
    enable_private_nodes = true
  }

  depends_on = [google_compute_router_nat.nat-gateway]
}
