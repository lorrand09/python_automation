import os
from typing import Dict


class APIConfig:
    FOOTBALL_API_BASE_URL = "https://football98.p.rapidapi.com"

    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_api_key_here")
    RAPIDAPI_HOST = "football98.p.rapidapi.com"

    HEADERS = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}

    ENDPOINTS = {
        "competitions": "/competitions",
        "teams": "/teams",
    }

    TEST_COMPETITIONS = ["liga", "premierleague", "seriea", "bundesliga"]

    TIMEOUT = 10

    @classmethod
    def get_endpoint_url(cls, endpoint: str, **kwargs) -> str:
        """Build full URL for endpoint with parameters"""
        path = cls.ENDPOINTS.get(endpoint, "")
        if kwargs:
            path = path.format(**kwargs)
        return f"{cls.FOOTBALL_API_BASE_URL}{path}"
