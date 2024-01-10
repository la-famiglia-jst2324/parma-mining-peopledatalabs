"""Main entrypoint for the API routes in of parma-analytics."""
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, status

from parma_mining.client import PdlClient
from parma_mining.model import CompaniesRequest, OrganizationModel

env = os.getenv("env", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

base_url = str(os.getenv("PDL_BASE_URL") or "")
api_key = str(os.getenv("PDL_API_KEY") or "")
api_version = str(os.getenv("PDL_API_VERSION") or "")

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-peopledatalabs"}


@app.post(
    "/organizations",
    status_code=status.HTTP_200_OK,
    response_model=list[OrganizationModel],
)
def get_organization_details(companies: CompaniesRequest) -> list[OrganizationModel]:
    """API Endpoint for the organization details according to the company domains.

    Possible types : "name" and "website"
    """
    _pdl_client = PdlClient(api_key, api_version, base_url)
    all_org_details = []
    for company_name, company_identifiers in companies.companies.items():
        for company_identifier in company_identifiers:
            org_details = _pdl_client.get_organization_details(
                company_identifier, companies.type
            )
            all_org_details.append(org_details)

    return all_org_details
