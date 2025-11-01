import pytest
import allure


@allure.feature("Searching")
@allure.story("Search Functionality")
class TestSearchFunctionality:
    @allure.title("Search for a streamer - logged out")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.frontend
    def test_search_streamer(
        self, home_page, search_page, streamer_page, env_config, gestures, helpers
    ):
        title = "StarCraft II"

        home_page.navigate_to(env_config["base_url"])
        home_page.wait_for_home_page_to_load()
        home_page.click_browse()

        search_page.wait_for_search_page_to_load()
        search_page.input_text(search_page.selectors.SEARCH_INPUT_LABEL, title)

        gestures.scroll_down(2, 300)

        search_page.click_suggestion_by_title(title)
        streamer_page.wait_for_search_page_to_load()

        helpers.take_screenshot("streamer-page")
