from selenium.webdriver.common.by import By
from common.selectors.common import CommonSelectors


class HomePageSelectors(CommonSelectors):
    LIVE_ON_TWITCH_TITLE = (By.XPATH, "//span[text()='Live on Twitch']")
    BROWSE_BTN = (By.XPATH, "//div[text()='Browse']")
    HOME_BTN = (By.XPATH, "//div[text()='Home']")
    ACTIVITY_BTN = (By.XPATH, "//div[text()='Activity']")
    PROFILE_BTN = (By.XPATH, "//div[text()='Profile']")
