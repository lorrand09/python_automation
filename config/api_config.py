"""
API configuration for Football API tests.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from config.constants import (
    FOOTBALL_API_BASE_URL,
    RAPIDAPI_HOST,
    ENDPOINTS,
    API_TIMEOUT,
)

# Load .env file if it exists (for local development)
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Get API key from environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    raise ValueError(
        "RAPIDAPI_KEY environment variable is not set. "
        "Please create a .env file with RAPIDAPI_KEY or set it as an environment variable."
    )

# Build headers with the API key from environment
FOOTBALL_API_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
}


class APIConfig:
    """
    Configuration class for Football API settings.
    """

    FOOTBALL_API_BASE_URL = FOOTBALL_API_BASE_URL
    RAPIDAPI_KEY = RAPIDAPI_KEY
    RAPIDAPI_HOST = RAPIDAPI_HOST
    HEADERS = FOOTBALL_API_HEADERS
    ENDPOINTS = ENDPOINTS
    TIMEOUT = API_TIMEOUT

    @classmethod
    def get_endpoint_url(cls, endpoint: str, **kwargs) -> str:
        """
        Constructs full endpoint URL from endpoint key and parameters.
        """
        path = cls.ENDPOINTS.get(endpoint, "")
        if kwargs:
            path = path.format(**kwargs)
        return f"{cls.FOOTBALL_API_BASE_URL}{path}"
