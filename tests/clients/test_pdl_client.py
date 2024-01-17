from unittest.mock import patch

import httpx
import pytest

from parma_mining.mining_common.exceptions import CrawlingError
from parma_mining.peopledatalabs.client import PdlClient
from parma_mining.peopledatalabs.model import OrganizationModel


@pytest.fixture
def pdl_client():
    return PdlClient("dummy_api_key", "dummy_api_version", "dummy_base_url")


@patch("parma_mining.peopledatalabs.client.PdlClient.get")
def test_get_organization_details_success(mock_get, pdl_client: PdlClient):
    test_data = {
        "status": 200,
        "name": "TestOrg",
        "display_name": "test",
        "size": "test",
        "employee_count": 1,
        "id": "test",
        "founded": 1,
        "industry": "test",
        "naics": None,
        "sic": None,
        "location": {
            "name": "test",
            "locality": "test",
            "region": "test",
            "metro": "test",
            "country": "test",
            "continent": "test",
            "street_address": "test",
            "address_line_2": "test",
            "postal_code": "test",
            "geo": "test",
        },
        "linkedin_id": "test",
        "linkedin_url": "test",
        "facebook_url": "test",
        "twitter_url": "test",
        "profiles": [],
        "website": "test",
        "ticker": "test",
        "gics_sector": "test",
        "mic_exchange": "test",
        "type": "test",
        "summary": "test",
        "tags": [],
        "headline": "test",
        "alternative_names": [],
        "alternative_domains": [],
        "affiliated_profiles": [],
        "likelihood": 5,
    }

    mock_get.return_value = httpx.Response(
        request=httpx.Request("GET", "test"), json=test_data, status_code=200
    )

    result = pdl_client.get_organization_details("name", "TestOrg")

    assert isinstance(result, OrganizationModel)
    assert result.name == "TestOrg"


@patch("parma_mining.peopledatalabs.client.PdlClient.get")
def test_get_companies_by_list_exception(mock_get, pdl_client: PdlClient):
    exception_instance = CrawlingError("Error fetching organization details!")
    mock_get.side_effect = exception_instance
    with pytest.raises(CrawlingError):
        pdl_client.get_organization_details("name", "TestOrg")
