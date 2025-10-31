from selenium.webdriver.common.by import By


class CommonSelectors:
    COOKIE_ACCEPT_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-a-target='consent-banner-accept']",
    )
