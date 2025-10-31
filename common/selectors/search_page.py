from selenium.webdriver.common.by import By
from common.selectors.common import CommonSelectors


class SearchPageSelectors(CommonSelectors):
    SEARCH_INPUT_LABEL = (By.XPATH, "//input[@type='search']")
    HEADER = (By.XPATH, "//*[@id='twilight-sticky-header-root']")
