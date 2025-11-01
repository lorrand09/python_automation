import requests
import allure
from typing import Dict, Optional, Any
from config.api_config import APIConfig
import json


class FootballAPIClient:
    def __init__(self):
        self.base_url = APIConfig.FOOTBALL_API_BASE_URL
        self.headers = APIConfig.HEADERS
        self.timeout = APIConfig.TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs,
    ) -> requests.Response:
        """Make the HTTP request together with Allure logging"""

        url = f"{self.base_url}{endpoint}"

        # Log request details to Allure
        with allure.step(f"{method} {endpoint}"):
            allure.attach(
                json.dumps({"url": url, "params": params, "data": data}, indent=2),
                name="Request Details",
                attachment_type=allure.attachment_type.JSON,
            )

            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout,
                    **kwargs,
                )

                if response.content:
                    try:
                        allure.attach(
                            json.dumps(response.json(), indent=2),
                            name="Response Body",
                            attachment_type=allure.attachment_type.JSON,
                        )
                    except json.JSONDecodeError:
                        allure.attach(
                            response.text,
                            name="Response Body",
                            attachment_type=allure.attachment_type.TEXT,
                        )

                allure.attach(
                    str(response.status_code),
                    name="Status Code",
                    attachment_type=allure.attachment_type.TEXT,
                )

                return response

            except requests.exceptions.RequestException as e:
                allure.attach(
                    str(e),
                    name="Request Error",
                    attachment_type=allure.attachment_type.TEXT,
                )
                raise

    def get_competitions(self) -> requests.Response:
        return self._make_request("GET", "/competitions")
