from selenium.webdriver.common.by import By

from common.pages.common import CommonPage
from common.selectors.streamer_page import StreamerPageSelectors


class StreamerPage(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.selectors = StreamerPageSelectors()

    def wait_for_search_page_to_load(self):
        self.wait_for_element_visible(self.selectors.FOLLOW_BTN)
