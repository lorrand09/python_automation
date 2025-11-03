"""
HomePage page object for home page interactions.
"""

from common.pages.common import CommonPage
from common.selectors.home_page import HomePageSelectors


class HomePage(CommonPage):
    """
    Page object for home page functionality.
    """

    def __init__(self, driver):
        """
        Initialize HomePage with driver and selectors.
        """
        super().__init__(driver)
        self.selectors = HomePageSelectors()

    def wait_for_home_page_to_load(self):
        """
        Wait for all key home page elements to be visible.
        """
        self.accept_cookies_if_present()
        self.wait_for_element_visible(self.selectors.LIVE_ON_TWITCH_TITLE)
        self.wait_for_element_visible(self.selectors.HOME_BTN)
        self.wait_for_element_visible(self.selectors.BROWSE_BTN)
        self.wait_for_element_visible(self.selectors.ACTIVITY_BTN)
        self.wait_for_element_visible(self.selectors.PROFILE_BTN)

    def click_browse(self):
        """
        Click the Browse button.
        """
        self.click(self.selectors.BROWSE_BTN)

    def click_home(self):
        """
        Click the Home button.
        """
        self.click(self.selectors.HOME_BTN)
