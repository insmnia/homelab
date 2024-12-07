terraform {
  backend "gcs" {
    bucket  = "homelab-terraform-state-bucket"
    prefix  = "terraform/state"
  }
}
