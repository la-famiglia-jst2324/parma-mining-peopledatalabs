from unittest.mock import patch

import httpx
import pytest

from parma_mining.mining_common.const import HTTP_200, HTTP_500
from parma_mining.peopledatalabs.analytics_client import AnalyticsClient
from parma_mining.peopledatalabs.model import OrganizationModel, ResponseModel

TOKEN = "mocked_token"


@pytest.fixture
def analytics_client():
    return AnalyticsClient()


@pytest.fixture
def mock_organization_model():
    return OrganizationModel.model_validate(
        {
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
    )


@pytest.fixture
def mock_response_model(mock_organization_model):
    return ResponseModel(
        source_name="TestSource",
        company_id="TestCompany",
        raw_data=mock_organization_model,
    )


@patch("httpx.post")
def test_send_post_request_success(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"key": "value"})
    response = analytics_client.send_post_request(
        TOKEN, "http://example.com", {"data": "test"}
    )
    assert response == {"key": "value"}


@patch("httpx.post")
def test_send_post_request_failure(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_500, text="Internal Server Error")
    with pytest.raises(Exception) as exc_info:
        analytics_client.send_post_request(
            TOKEN, "http://example.com", {"data": "test"}
        )
    assert "API request failed" in str(exc_info.value)


@patch("httpx.post")
def test_register_measurements(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"id": "123"})
    mapping = {"Mappings": [{"DataType": "int", "MeasurementName": "test_metric"}]}
    result, updated_mapping = analytics_client.register_measurements(TOKEN, mapping)
    assert "source_measurement_id" in updated_mapping["Mappings"][0]
    assert result[0]["source_measurement_id"] == "123"


@patch("httpx.post")
def test_feed_raw_data(mock_post, analytics_client, mock_response_model):
    mock_post.return_value = httpx.Response(HTTP_200, json={"result": "success"})
    result = analytics_client.feed_raw_data(TOKEN, mock_response_model)
    assert result == {"result": "success"}
