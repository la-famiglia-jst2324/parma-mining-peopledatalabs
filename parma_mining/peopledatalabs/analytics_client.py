"""Client for Analytics module."""
import json
import os
import urllib.parse

import httpx
from dotenv import load_dotenv

from parma_mining.mining_common.exceptions import AnalyticsError
from parma_mining.peopledatalabs.model import ResponseModel


class AnalyticsClient:
    """Class for the Analytics Client."""

    load_dotenv()

    analytics_base = str(os.getenv("ANALYTICS_BASE_URL") or "")

    measurement_url = urllib.parse.urljoin(analytics_base, "/source-measurement")
    feed_raw_url = urllib.parse.urljoin(analytics_base, "/feed-raw-data")
    crawling_finished_url = urllib.parse.urljoin(analytics_base, "/crawling-finished")

    def send_post_request(self, api_endpoint, data):
        """POST method for the Analytics API's."""
        headers = {
            "Content-Type": "application/json",
        }

        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise AnalyticsError(
                f"API request failed with status code {response.status_code},"
                f"response: {response.text}"
            )

    def register_measurements(self, mapping, parent_id=None, source_module_id=None):
        """Method for registering the measurements."""
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_data = {
                "source_module_id": source_module_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }

            if parent_id is not None:
                measurement_data["parent_measurement_id"] = parent_id

            response = self.send_post_request(self.measurement_url, measurement_data)
            measurement_data["source_measurement_id"] = response.get("id")

            # add the source measurement id to mapping
            field_mapping["source_measurement_id"] = measurement_data[
                "source_measurement_id"
            ]

            if "NestedMappings" in field_mapping:
                nested_measurements = self.register_measurements(
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_data["source_measurement_id"],
                    source_module_id=source_module_id,
                )[0]
                result.extend(nested_measurements)
            result.append(measurement_data)
        return result, mapping

    def feed_raw_data(self, input_data: ResponseModel):
        """Methods for sending the raw data to the analytics."""
        organization_json = json.loads(input_data.raw_data.model_dump_json())

        data = {
            "source_name": input_data.source_name,
            "company_id": input_data.company_id,
            "raw_data": organization_json,
        }

        return self.send_post_request(self.feed_raw_url, data)

    def crawling_finished(self, data):
        """Notify crawling is finished to the analytics."""
        return self.send_post_request(self.crawling_finished_url, data)
