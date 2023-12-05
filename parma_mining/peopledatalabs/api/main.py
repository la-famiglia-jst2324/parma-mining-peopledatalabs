"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status
from dotenv import load_dotenv
import os
from typing import List
from parma_mining.client import PdlClient
from parma_mining.model import OrganizationModel, CompaniesRequest


load_dotenv()

base_url = str(os.getenv("PDL_BASE_URL") or "")
api_key = str(os.getenv("PDL_API_KEY") or "")
api_version = str(os.getenv("PDL_API_VERSION") or "")

app = FastAPI()


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-peopledatalabs"}


@app.post(
    "/organizations",
    status_code=status.HTTP_200_OK,
    response_model=List[OrganizationModel],
)
def get_organization_details(companies: CompaniesRequest) -> List[OrganizationModel]:
    """API Endpoint for the organization details according to the company domains.

    Possible types : "name" and "website"
    """
    _pdlClient = PdlClient(api_key, api_version, base_url)
    all_org_details = []
    for company_name, company_identifiers in companies.companies.items():
        for company_identifier in company_identifiers:
            org_details = _pdlClient.get_organization_details(
                company_identifier, companies.type
            )
            all_org_details.append(org_details)

    return all_org_details
