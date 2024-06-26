import logging
from unittest.mock import MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient

from parma_mining.mining_common.const import HTTP_200
from parma_mining.peopledatalabs.api.dependencies.auth import authenticate
from parma_mining.peopledatalabs.api.main import app
from tests.dependencies.mock_auth import mock_authenticate


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


@pytest.fixture
def mock_pdl_client(mocker) -> MagicMock:
    test_data = {
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
    mock_get = mocker.patch("parma_mining.peopledatalabs.api.main.PdlClient.get")
    mock_get.return_value = httpx.Response(
        request=httpx.Request("GET", "test"), json=test_data, status_code=200
    )

    return mock_get


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticClient's method to avoid actual API calls during testing."""
    mock = mocker.patch(
        "parma_mining.peopledatalabs.api.main.AnalyticsClient.feed_raw_data"
    )
    mock = mocker.patch(
        "parma_mining.peopledatalabs.api.main.AnalyticsClient.crawling_finished"
    )
    mock.return_value = {}
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_companies_success(
    client: TestClient, mock_pdl_client: MagicMock, mock_analytics_client: MagicMock
):
    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        },
    }
    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)

    mock_analytics_client.assert_called()
    mock_pdl_client.assert_called()
    assert response.status_code == HTTP_200
