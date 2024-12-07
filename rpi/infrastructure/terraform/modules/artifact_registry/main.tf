resource "google_project_service" "gcp_artifact_registry_api" {
  project = var.project_id
  service = "artifactregistry.googleapis.com"
}

resource "google_artifact_registry_repository" "this" {
  provider = google

  project = var.project_id
  repository_id = var.repository_id
  format        = var.format
  location      = var.location
  description   = var.description
  depends_on = [ google_project_service.gcp_artifact_registry_api ]
}
