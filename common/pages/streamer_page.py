"""
StreamerPage page object for streamer profile interactions.
"""

from selenium.webdriver.common.by import By

from common.pages.common import CommonPage
from common.selectors.streamer_page import StreamerPageSelectors


class StreamerPage(CommonPage):
    """
    Page object for streamer page functionality.
    """

    def __init__(self, driver):
        """
        Initialize StreamerPage with driver and selectors.
        """
        super().__init__(driver)
        self.selectors = StreamerPageSelectors()

    def wait_for_search_page_to_load(self):
        """
        Wait for streamer page to load by checking Follow button visibility.
        """
        self.wait_for_element_visible(self.selectors.FOLLOW_BTN)
