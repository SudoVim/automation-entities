"""
module containing logic for creating the selenium webdriver
"""
from typing import Literal, Optional

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

Browser = Literal["chrome"]


def create_chrome_webdriver(
    headless: bool = False,
    user_data_dir: Optional[str] = None,
) -> webdriver.Chrome:
    """
    Create and return a chrome webdriver from the given arguments.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disble-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    if headless:
        options.add_argument("--headless")

    return webdriver.Chrome(
        options=options,
    )


def create_webdriver(
    browser: Browser, headless: bool = False, user_data_dir: Optional[str] = None
) -> WebDriver:
    """
    Create a webdriver from the given arguments.
    """
    if browser == "chrome":
        return create_chrome_webdriver(headless=headless, user_data_dir=user_data_dir)

    assert False, f"invalid browser type {browser}"
