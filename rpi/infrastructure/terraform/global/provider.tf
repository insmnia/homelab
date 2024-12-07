variable "CRED_PATH" {
  type = string
}


provider "google" {
  credentials = file(var.CRED_PATH)
  project     = var.project_id
  region      = var.region
}
