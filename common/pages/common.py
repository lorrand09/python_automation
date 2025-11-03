"""
Base page class with common page operations.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from common.selectors.common import CommonSelectors


class CommonPage:
    """
    Base page class providing common page interaction methods.
    """

    def __init__(self, driver, timeout=15):
        """
        Initialize page with driver and default timeout.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to(self, url):
        """
        Navigate to URL and wait for page to load completely.
        """
        self.driver.get(url)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible and return it.
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            element = wait.until(ec.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            by, value = locator
            raise TimeoutException(
                f"Element not visible within {timeout or 10} seconds.\n"
                f"  Locator: {by} = '{value}'\n"
                f"  Current URL: {self.driver.current_url}"
            )

    def is_element_displayed(self, locator, timeout=5):
        """
        Check if element is displayed within timeout period.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
            return False

    def verify_text_equals(self, locator, expected_text):
        """
        Verify element text matches expected text.
        """
        element = self.wait_for_element_visible(locator)
        actual_text = element.text.strip()
        expected_text = expected_text.strip()

        assert (
            actual_text == expected_text
        ), f"Text mismatch!\n  Expected: '{expected_text}'\n  Actual: '{actual_text}'"

    def click(self, locator):
        """
        Wait for element to be clickable and click it.
        """
        element = self.wait.until(ec.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text):
        """
        Clear and input text into element.
        """
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """
        Get text content from element.
        """
        element = self.wait_for_element_visible(locator)
        return element.text.strip()

    def accept_cookies_if_present(self, timeout=2):
        """
        Accept cookies if banner is displayed, otherwise continue without error.
        """
        try:
            cookie_button = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(CommonSelectors.COOKIE_ACCEPT_BUTTON)
            )
            cookie_button.click()
        except (TimeoutException, Exception):
            pass
