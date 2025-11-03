"""
Pytest Configuration File - Central Fixture Definitions
"""

import pytest
import sys
from pathlib import Path

from config.driver import DriverFactory
from config.config import Config
from utils.gestures import Gestures
from utils.helpers import Helpers
from api.football.client import FootballAPIClient
from config.api_config import APIConfig
from config.constants import TEST_COMPETITIONS

sys.path.append(str(Path(__file__).parent.parent.parent))


@pytest.fixture(scope="function")
def driver():
    """
    Provides WebDriver instance for UI testing.
    Creates new driver for each test and quits after test completion.
    """
    driver_instance = DriverFactory.get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def env_config():
    """
    Loads and provides environment configuration settings.
    """
    config = Config.load_environment_config()
    return {
        "base_url": config.get("base_url", ""),
    }


@pytest.fixture
def gestures(driver):
    """
    Provides gesture utilities for mobile/touch interactions.
    """
    return Gestures(driver)


@pytest.fixture
def helpers(driver):
    """
    Provides general helper utilities for test operations.
    """
    return Helpers(driver)


@pytest.fixture
def home_page(driver):
    """
    Provides HomePage page object for home page interactions.
    """
    from common.pages.home_page import HomePage

    return HomePage(driver)


@pytest.fixture
def search_page(driver):
    """
    Provides SearchPage page object for search functionality.
    """
    from common.pages.search_page import SearchPage

    return SearchPage(driver)


@pytest.fixture
def streamer_page(driver):
    """
    Provides StreamerPage page object for streamer profile interactions.
    """
    from common.pages.streamer_page import StreamerPage

    return StreamerPage(driver)


@pytest.fixture(scope="session")
def api_client():
    """
    Provides Football API client for making API requests.
    Single instance shared across all tests.
    """
    return FootballAPIClient()


@pytest.fixture(scope="session")
def api_config():
    """
    Provides API configuration settings.
    """
    return APIConfig


@pytest.fixture
def competitions():
    """
    Provides test data dictionary with competition IDs.
    """
    return TEST_COMPETITIONS
