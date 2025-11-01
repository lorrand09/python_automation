import pytest
import allure
import json
from http import HTTPStatus


@allure.feature("Football Data API")
class TestFootballAPI:
    @allure.story("Competitions")
    @allure.title("Get all available competitions")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_competitions(self, api_client):
        with allure.step("Send GET request to competitions endpoint"):
            response = api_client.get_competitions()

        with allure.step("Validate response status"):
            assert (
                response.status_code == HTTPStatus.OK
            ), f"Expected 200, got {response.status_code}"

        with allure.step("Validate response structure"):
            data = response.json()

            # Parse the competition names string, remove curly braces and split by comma
            competitions_str = data.strip("{}")
            competitions = competitions_str.split(",")

            assert len(competitions) > 0, "Should return at least one competition"

            assert "bundesliga" in competitions, "Should include bundesliga"
            assert "premierleague" in competitions, "Should include premier league"

            allure.attach(
                f"Found {len(competitions)} competitions",
                name="Competition Count",
                attachment_type=allure.attachment_type.TEXT,
            )
