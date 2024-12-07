terraform {
  backend "gcs" {
    bucket  = "homelab-terraform-state-bucket"
    prefix  = "terraform/state"
  }
}

module "artifact_registry" {
  source       = "../../modules/artifact_registry"
  repository_id = "homelab-dev-registry"
  location      = var.region
  description   = "Development Artifact Registry repository"
  project_id = var.project_id
}
