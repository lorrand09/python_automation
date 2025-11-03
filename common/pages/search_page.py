"""
SearchPage page object for search functionality.
"""

from selenium.webdriver.common.by import By

from common.pages.common import CommonPage
from common.selectors.search_page import SearchPageSelectors


class SearchPage(CommonPage):
    """
    Page object for search page functionality.
    """

    def __init__(self, driver):
        """
        Initialize SearchPage with driver and selectors.
        """
        super().__init__(driver)
        self.selectors = SearchPageSelectors()

    def wait_for_search_page_to_load(self):
        """
        Wait for search page header to be visible.
        """
        self.wait_for_element_visible(self.selectors.HEADER)

    def click_search_bar(self):
        """
        Click the search input field.
        """
        self.click(self.selectors.SEARCH_INPUT_LABEL)

    def click_suggestion_by_title(self, title):
        """
        Click search suggestion matching the given title.
        """
        streamer_title = f"//p[@title='{title}']"
        element = self.driver.find_element(By.XPATH, streamer_title)
        element.click()
