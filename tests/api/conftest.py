import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import pytest
from api.client.football import FootballAPIClient
from config.api_config import APIConfig


@pytest.fixture(scope="session")
def api_client():
    return FootballAPIClient()


@pytest.fixture(scope="session")
def api_config():
    return APIConfig()


@pytest.fixture
def competitions():
    return APIConfig.TEST_COMPETITIONS
