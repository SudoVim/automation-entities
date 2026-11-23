"""
module containing logic for creating the selenium webdriver
"""

import os
from typing import Literal, Optional

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from .patcher import Patcher

Browser = Literal["chrome", "undetected-chrome"]


def create_chrome_webdriver(
    headless: bool = False,
    user_data_dir: Optional[str] = None,
    user_agent: Optional[str] = None,
    use_undetected: bool = False,
) -> webdriver.Chrome:
    """
    Create and return a chrome webdriver from the given arguments.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disble-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    if headless:
        options.add_argument("--headless")

    if use_undetected:
        driver_executable_path = patch_undetected()
        return uc.Chrome(
            options=options,
            driver_executable_path=driver_executable_path,
        )

    return webdriver.Chrome(options=options)


def patch_undetected():
    """
    Pre-patch the "undetected" chromedriver. This'll figure out the chrome
    executable that we're going to use and pre-patch it so that the
    "undetected_chromedriver" module doesn't try to do this itself and bungle
    it.
    """
    patcher = Patcher()
    return patcher.find_patch_chromedriver()


def create_webdriver(
    browser: Browser,
    headless: bool = False,
    user_data_dir: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> WebDriver:
    """
    Create a webdriver from the given arguments.
    """
    if browser == "chrome":
        return create_chrome_webdriver(
            headless=headless,
            user_data_dir=user_data_dir,
            user_agent=user_agent,
        )

    if browser == "undetected-chrome":
        return create_chrome_webdriver(
            headless=headless,
            user_data_dir=user_data_dir,
            user_agent=user_agent,
            use_undetected=True,
        )
