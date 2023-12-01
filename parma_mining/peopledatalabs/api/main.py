"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status
from dotenv import load_dotenv
import os

from parma_mining.client import PdlClient
from parma_mining.model import OrganizationModel


load_dotenv()

base_url = str(os.getenv("PDL_BASE_URL") or "")
api_key = str(os.getenv("PDL_API_KEY") or "")

app = FastAPI()


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-peopledatalabs"}


@app.get("/organization/{org_domain}", status_code=status.HTTP_200_OK)
def get_organization_details(org_domain: str) -> OrganizationModel:
    """API Endpoint for the organization details according to the company domain.

    Ex : "google.com"
    """
    _pdlClient = PdlClient(api_key, base_url)
    return _pdlClient.get_organization_details(org_domain)
