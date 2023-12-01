import httpx
from httpx import Response
from parma_mining.model import OrganizationModel
from urllib.parse import urljoin
from fastapi import HTTPException, status


class PdlClient:
    def __init__(self, api_key: str, api_version: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version

    def get(self, path: str, query: dict[str, str]) -> Response:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }
        full_path = urljoin(self.base_url, self.api_version + path)
        return httpx.request("GET", url=full_path, headers=headers, params=query)

    def get_organization_details(self, org_domain: str) -> OrganizationModel:
        query = {"website": org_domain}
        path = "/company/enrich"

        response = self.get(path, query)
        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
            )

        parsed_organization = OrganizationModel.model_validate(response.json())
        return parsed_organization
