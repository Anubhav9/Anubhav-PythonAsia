resource "google_container_cluster" "python_asia_cluster" {
  name = "${var.python_asia_nomenclature}-cluster"
  network = google_compute_network.python_asia_vpc.id
  subnetwork = google_compute_subnetwork.python_asia_subnet.id
  remove_default_node_pool = true
  initial_node_count       = 1
  
}

resource "google_container_node_pool" "public_node" {
  name = "${var.python_asia_nomenclature}-public-node"
  location = "asia-northeast2"
  cluster = google_container_cluster.python_asia_cluster.id
  node_count = 1
  node_locations = ["asia-northeast2-c"]

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    labels = {
      env = "dev"
    }

  }
  
}

resource "google_container_node_pool" "private_node" {
  name = "${var.python_asia_nomenclature}-private-node"
  location = "asia-northeast2"
  cluster = google_container_cluster.python_asia_cluster.id
  node_count = 1
  node_locations = ["asia-northeast2-c"]

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    labels = {
      env = "dev"
    }

  }
  network_config {
    enable_private_nodes = true
  }
  
}