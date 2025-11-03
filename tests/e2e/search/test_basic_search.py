"""
frontend e2e test for search functionality.
"""

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
        """
        Verify user can search for a streamer and navigate to their page while logged out.

        Steps:
        1. Navigate to home page
        2. Click browse button
        3. Enter search query
        4. Scroll down 2 times
        5. Select streamer based on its title
        6. Wait for streamer page to load
        7. Take screenshot of the streamer page
        """
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
