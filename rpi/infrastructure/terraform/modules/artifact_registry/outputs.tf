output "repository_id" {
  value = google_artifact_registry_repository.this.repository_id
  description = "The ID of the Artifact Registry repository."
}
