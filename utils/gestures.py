import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Gestures:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def scroll_down(self, times=2, pixels=300):
        """
        Scroll down by specified pixels, multiple times.
        """
        for i in range(times):
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            time.sleep(0.5)

    def scroll_up(self, times=1, pixels=300):
        """
        Scroll up by specified pixels, multiple times.
        """
        for i in range(times):
            self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            time.sleep(0.5)
