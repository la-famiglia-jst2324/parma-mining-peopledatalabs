"""Main entrypoint for the API routes in of parma-analytics."""

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, status

from parma_mining.peopledatalabs.analytics_client import AnalyticsClient
from parma_mining.peopledatalabs.client import PdlClient
from parma_mining.peopledatalabs.model import (
    CompaniesRequest,
    DiscoveryModel,
    ResponseModel,
)
from parma_mining.peopledatalabs.normalization_map import PdlNormalizationMap

load_dotenv()

base_url = str(os.getenv("PDL_BASE_URL") or "")
api_key = str(os.getenv("PDL_API_KEY") or "")
api_version = str(os.getenv("PDL_API_VERSION") or "")

app = FastAPI()

analytics_client = AnalyticsClient()
normalization = PdlNormalizationMap()


# root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-peopledatalabs"}


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "monthly"
    normalization_map = normalization.get_normalization_map()
    # register the measurement to analytics
    analytics_client.register_measurements(
        normalization_map, source_module_id=source_id
    )

    # set and return results
    results = {}
    results["frequency"] = time
    results["normalization_map"] = str(normalization_map)
    return json.dumps(results)


@app.post(
    "/companies",
    status_code=status.HTTP_200_OK,
)
def get_organization_details(companies: CompaniesRequest):
    """API Endpoint for the organization details according to the company domains.

    Possible types : "name" and "website"
    """
    pdl_client = PdlClient(api_key, api_version, base_url)
    for company_id, company_data in companies.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                org_details = pdl_client.get_organization_details(handle, data_type)
                data = ResponseModel(
                    source_name="peopledatalabs",
                    company_id=company_id,
                    raw_data=org_details,
                )
                try:
                    analytics_client.feed_raw_data(data)
                except Exception:
                    raise Exception("Can't send crawling data to the Analytics.")

    return org_details


@app.get(
    "/discover",
    response_model=list[DiscoveryModel],
    status_code=status.HTTP_200_OK,
)
def search_organizations(query: str) -> list[DiscoveryModel]:
    """Discovery endpoint for the API."""
    # Return same name only to agree with the common interface among data sources
    # There is no discover for PDL
    result = [DiscoveryModel.model_validate({"name": query, "handle": query})]
    return result
