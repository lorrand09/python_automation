import os
from datetime import datetime


class Helpers:
    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, name):
        """
        Take a screenshot and save it to reports/screenshots directory
        """
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()
        filename = f"{name}_{datetime.now()}.png"

        filepath = os.path.join(screenshot_dir, filename)
        screenshot = self.driver.get_screenshot_as_png()

        with open(filepath, "wb") as f:
            f.write(screenshot)

        print(f"Screenshot saved: {filepath}")
        return filepath
