"""
WebDriver Factory for creating browser driver instances.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config


class DriverFactory:
    @staticmethod
    def get_driver():
        """
        Creates and returns WebDriver instance based on configuration.
        """
        browser = Config.BROWSER.lower()
        device_type = Config.DEVICE_TYPE.lower()

        if browser == "chrome":
            return DriverFactory._get_chrome_driver(device_type)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_chrome_driver(device_type):
        """
        Creates Chrome WebDriver with specified device type (desktop/mobile).
        """
        options = webdriver.ChromeOptions()

        if Config.HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        if device_type == "mobile":
            mobile_emulation = {"deviceName": "iPhone 12 Pro"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

        if device_type == "desktop":
            driver.maximize_window()

        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver
