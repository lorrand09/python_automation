import pytest
from config.driver import DriverFactory
from config.config import Config
from utils.gestures import Gestures
from utils.helpers import Helpers


@pytest.fixture(scope="function")
def driver():
    driver_instance = DriverFactory.get_driver()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def env_config():
    config = Config.load_environment_config()
    return {
        "base_url": config.get("base_url", ""),
    }


@pytest.fixture
def gestures(driver):
    return Gestures(driver)


@pytest.fixture
def helpers(driver):
    return Helpers(driver)


@pytest.fixture
def home_page(driver):
    from common.pages.home_page import HomePage

    return HomePage(driver)


@pytest.fixture
def search_page(driver):
    from common.pages.search_page import SearchPage

    return SearchPage(driver)


@pytest.fixture
def streamer_page(driver):
    from common.pages.streamer_page import StreamerPage

    return StreamerPage(driver)
