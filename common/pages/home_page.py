from common.pages.common import CommonPage
from common.selectors.home_page import HomePageSelectors


class HomePage(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.selectors = HomePageSelectors()

    def wait_for_home_page_to_load(self):
        self.accept_cookies_if_present()
        self.wait_for_element_visible(self.selectors.LIVE_ON_TWITCH_TITLE)
        self.wait_for_element_visible(self.selectors.HOME_BTN)
        self.wait_for_element_visible(self.selectors.BROWSE_BTN)
        self.wait_for_element_visible(self.selectors.ACTIVITY_BTN)
        self.wait_for_element_visible(self.selectors.PROFILE_BTN)

    def click_browse(self):
        self.click(self.selectors.BROWSE_BTN)

    def click_home(self):
        self.click(self.selectors.HOME_BTN)
