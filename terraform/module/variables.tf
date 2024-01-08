variable "env" {
  description = "staging or prod environment"
  type        = string
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
}

variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}

/* ------------------------ Analytics and Sourcing Auth Flow ------------------------ */

variable "SHARED_SECRET_KEY" {
  description = "Shared secret key for the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}

/* -------------------------------- People Data Labs -------------------------------- */

variable "PDL_API_KEY" {
  description = "value"
  type        = string
  sensitive   = true
}

variable "PDL_API_VERSION" {
  description = "value"
  type        = string
}

variable "PDL_BASE_URL" {
  description = "value"
  type        = string
}
