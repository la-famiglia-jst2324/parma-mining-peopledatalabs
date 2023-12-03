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

variable "FIREBASE_ADMINSDK_CERTIFICATE" {
  description = "value"
  type        = string
  sensitive   = true
}

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
