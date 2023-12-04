
/* ---------------------------------- Service Image --------------------------------- */

# Note: Generally it is NOT best practise to build images in Terraform. We are still
# doing it here for simplicity. In industry, you should think twice before doing this.
resource "null_resource" "docker_build" {

  provisioner "local-exec" {
    working_dir = path.module
    command     = "IMG=${var.region}-docker.pkg.dev/${var.project}/parma-registry/parma-mining-peopledatalabs:${var.env}-$(git rev-parse --short HEAD) && docker build -t $IMG ./../../ && docker push $IMG && echo $IMG > .image.name"
  }

  triggers = {
    always_run = timestamp()
  }
}

# get output from docker_build
data "local_file" "image_name" {
  filename   = "${path.module}/.image.name"
  depends_on = [null_resource.docker_build]
}


/* ------------------------------------ Cloud Run ----------------------------------- */

resource "google_cloud_run_service" "parma_mining_peopledatalabs_cloud_run" {
  name     = "parma-mining-peopledatalabs-${var.env}"
  location = var.region

  template {
    spec {
      containers {
        image = data.local_file.image_name.content
        ports {
          container_port = 8080
        }
        env {
          name  = "FIREBASE_ADMINSDK_CERTIFICATE"
          value = var.FIREBASE_ADMINSDK_CERTIFICATE
        }
        env {
          name  = "PDL_API_KEY"
          value = var.PDL_API_KEY
        }
        env {
          name  = "PDL_API_VERSION"
          value = var.PDL_API_VERSION
        }
        env {
          name  = "PDL_BASE_URL"
          value = var.PDL_BASE_URL
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

/* --------------------------------------- IAM -------------------------------------- */

// Define a policy that allows any user to invoke the Cloud Run service.
data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

// Apply the policy to the Cloud Run service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.parma_mining_peopledatalabs_cloud_run.location
  project  = google_cloud_run_service.parma_mining_peopledatalabs_cloud_run.project
  service  = google_cloud_run_service.parma_mining_peopledatalabs_cloud_run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}