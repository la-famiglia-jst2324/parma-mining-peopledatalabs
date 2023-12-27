terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/staging/mining/peopledatalabs"
    credentials = "../.secrets/la-famiglia-parma-ai.json"
  }
}

locals {
  project = "la-famiglia-parma-ai"
  region  = "europe-west1"
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = local.project
  region      = local.region
}

module "main" {
  source                        = "../module"
  env                           = "staging"
  project                       = local.project
  region                        = local.region
  PDL_API_KEY                   = var.PDL_API_KEY
  PDL_API_VERSION               = var.PDL_API_VERSION
  PDL_BASE_URL                  = var.PDL_BASE_URL
  ANALYTICS_BASE_URL            = var.ANALYTICS_BASE_URL
}
