"""Client for the PDL API."""
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException
from httpx import Response

from parma_mining.mining_common.const import HTTP_400, HTTP_404
from parma_mining.peopledatalabs.model import OrganizationModel


class PdlClient:
    """Client for PDL API."""

    def __init__(self, api_key: str, api_version: str, base_url: str):
        """Initialize the PdlClient."""
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version

    def get(self, path: str, query: dict[str, str]) -> Response:
        """Make a GET request to the PDL API."""
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }
        full_path = urljoin(self.base_url, self.api_version + path)
        return httpx.request("GET", url=full_path, headers=headers, params=query)

    def get_organization_details(
        self, org_identifier: str, identifier_type: str
    ) -> OrganizationModel:
        """Fetch organization details from PDL."""
        query = {identifier_type: org_identifier}
        path = "/company/enrich"

        try:
            response = self.get(path, query)
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == HTTP_404:
                error_detail = "Organization not found."
            if exc.response.status_code == HTTP_400:
                error_detail = (
                    "Type not found. "
                    "Please use 'name' or 'website'"
                    "as a type in the request body."
                )
            else:
                error_detail = str(exc)
            raise HTTPException(
                status_code=exc.response.status_code, detail=error_detail
            )

        parsed_organization = OrganizationModel.model_validate(response.json())
        return parsed_organization
