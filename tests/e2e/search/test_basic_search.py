import pytest
from common.pages.home_page import HomePage
from common.pages.search_page import SearchPage
from common.pages.streamer_page import StreamerPage
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


class TestSearchFunctionality:
    @pytest.mark.smoke
    def test_search_streamer(self, driver, env_config, gestures, helpers):
        title = "StarCraft II"
        home_page = HomePage(driver)
        home_page.navigate_to(env_config["base_url"])
        home_page.wait_for_home_page_to_load()

        home_page.click_browse()

        search_page = SearchPage(driver)
        search_page.wait_for_search_page_to_load()
        search_page.input_text(search_page.selectors.SEARCH_INPUT_LABEL, title)

        gestures.scroll_down(2, 300)

        search_page.click_suggestion_by_title(title)
        streamer_page = StreamerPage(driver)
        streamer_page.wait_for_search_page_to_load()

        helpers.take_screenshot("streamer-page")
