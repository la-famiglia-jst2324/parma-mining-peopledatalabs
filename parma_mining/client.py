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

        try:
            response = self.get(path, query)
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                error_detail = "Organization not found."
            else:
                error_detail = str(exc)
            raise HTTPException(
                status_code=exc.response.status_code, detail=error_detail
            )

        parsed_organization = OrganizationModel.model_validate(response.json())
        return parsed_organization
