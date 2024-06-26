"""Main entrypoint for the API routes in of parma-analytics."""

import json
import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status

from parma_mining.mining_common.exceptions import (
    AnalyticsError,
    ClientInvalidBodyError,
    CrawlingError,
)
from parma_mining.peopledatalabs.analytics_client import AnalyticsClient
from parma_mining.peopledatalabs.api.dependencies.auth import authenticate
from parma_mining.peopledatalabs.client import PdlClient
from parma_mining.peopledatalabs.helper import collect_errors
from parma_mining.peopledatalabs.model import (
    CompaniesRequest,
    CrawlingFinishedInputModel,
    DiscoveryRequest,
    DiscoveryResponse,
    ErrorInfoModel,
    FinalDiscoveryResponse,
    ResponseModel,
)
from parma_mining.peopledatalabs.normalization_map import PdlNormalizationMap

env = os.getenv("DEPLOYMENT_ENV", "local")

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

analytics_client = AnalyticsClient()
normalization = PdlNormalizationMap()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-peopledatalabs"}


@app.get("/initialize", status_code=status.HTTP_200_OK)
def initialize(source_id: int, token=Depends(authenticate)) -> str:
    """Initialization endpoint for the API."""
    # init frequency
    time = "monthly"
    normalization_map = normalization.get_normalization_map()
    # register the measurement to analytics
    analytics_client.register_measurements(
        token, normalization_map, source_module_id=source_id
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
def get_organization_details(body: CompaniesRequest, token=Depends(authenticate)):
    """API Endpoint for the organization details according to the company domains.

    Possible types : "name" and "website"
    """
    errors: dict[str, ErrorInfoModel] = {}
    pdl_client = PdlClient(api_key, api_version, base_url)
    for company_id, company_data in body.companies.items():
        for data_type, handles in company_data.items():
            for handle in handles:
                try:
                    org_details = pdl_client.get_organization_details(handle, data_type)
                except CrawlingError as e:
                    logger.error(
                        f"Can't fetch company details from People Data Labs. Error: {e}"
                    )
                    collect_errors(company_id, errors, e)
                    continue

                data = ResponseModel(
                    source_name="peopledatalabs",
                    company_id=company_id,
                    raw_data=org_details,
                )
                try:
                    analytics_client.feed_raw_data(token, data)
                except AnalyticsError as e:
                    logger.error(
                        f"Can't send crawling data to the Analytics. Error: {e}"
                    )
                    collect_errors(company_id, errors, e)

    return analytics_client.crawling_finished(
        token,
        json.loads(
            CrawlingFinishedInputModel(
                task_id=body.task_id, errors=errors
            ).model_dump_json()
        ),
    )


@app.post(
    "/discover",
    response_model=FinalDiscoveryResponse,
    status_code=status.HTTP_200_OK,
)
def search_organizations(
    request: list[DiscoveryRequest], token: str = Depends(authenticate)
):
    """Discovery endpoint for the API."""
    if not request:
        msg = "Request body cannot be empty for discovery"
        logger.error(msg)
        raise ClientInvalidBodyError(msg)

    response_data = {}
    for company in request:
        logger.debug(
            f"Discovering with name: {company.name} for company_id {company.company_id}"
        )
        # Return same name only to agree with the common interface among data sources
        # There is no discover for PDL
        response = DiscoveryResponse(name=[company.name])
        response_data[company.company_id] = response

    current_date = datetime.now()
    valid_until = current_date + timedelta(days=180)

    return FinalDiscoveryResponse(identifiers=response_data, validity=valid_until)
