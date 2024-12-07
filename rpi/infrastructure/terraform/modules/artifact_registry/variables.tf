variable "project_id" {
  description = "The ID of the GCP Project"
  type        = string
}

variable "repository_id" {
  description = "The ID of the Artifact Registry repository"
  type        = string
}

variable "format" {
  description = "The format of the repository (DOCKER, NPM, etc.)"
  type        = string
  default     = "DOCKER"
}

variable "location" {
  description = "The location for the Artifact Registry repository"
  type        = string
}

variable "description" {
  description = "A description for the Artifact Registry repository"
  type        = string
  default     = "Production-grade Artifact Registry"
}
