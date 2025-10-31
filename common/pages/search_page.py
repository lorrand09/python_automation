from selenium.webdriver.common.by import By

from common.pages.common import CommonPage
from common.selectors.search_page import SearchPageSelectors


class SearchPage(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.selectors = SearchPageSelectors()

    def wait_for_search_page_to_load(self):
        self.wait_for_element_visible(self.selectors.HEADER)

    def click_search_bar(self):
        self.click(self.selectors.SEARCH_INPUT_LABEL)

    def click_suggestion_by_title(self, title):
        streamer_title = f"//p[@title='{title}']"
        element = self.driver.find_element(By.XPATH, streamer_title)
        element.click()
