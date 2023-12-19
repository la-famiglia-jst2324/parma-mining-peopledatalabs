from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200
from parma_mining.peopledatalabs.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_pdl_client(mocker) -> MagicMock:
    mock = mocker.patch(
        "parma_mining.peopledatalabs.api.main.PdlClient.get_organization_details"
    )
    mock.return_value = {
        "status": 200,
        "name": "test",
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
    return mock


def test_get_organization_details(mock_pdl_client: MagicMock):
    payload = {"companies": {"example_id": {"name": ["google"]}}}
    response = client.post("/companies", json=payload)
    print(response.json())
    assert response.status_code == HTTP_200
    assert response.json() == {
        "status": 200,
        "name": "test",
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
