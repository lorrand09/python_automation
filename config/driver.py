from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config


class DriverFactory:
    @staticmethod
    def get_driver():
        browser = Config.BROWSER.lower()
        device_type = Config.DEVICE_TYPE.lower()

        # This can be easily extended to other browsers too
        if browser == "chrome":
            return DriverFactory._get_chrome_driver(device_type)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_chrome_driver(device_type):
        options = webdriver.ChromeOptions()

        if Config.HEADLESS:
            options.add_argument("--headless=new")

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
