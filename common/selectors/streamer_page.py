from selenium.webdriver.common.by import By
from common.selectors.common import CommonSelectors


class StreamerPageSelectors(CommonSelectors):
    FOLLOW_BTN = (
        By.XPATH,
        "//button[@data-test-selector='follow-game-button-component']",
    )
