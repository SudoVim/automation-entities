"""
module containing logic for creating the selenium webdriver
"""

import subprocess
from distutils.version import LooseVersion
from typing import Literal, Optional

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

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
    chrome_executable = uc.find_chrome_executable()
    out = subprocess.check_output(
        [
            chrome_executable,
            "--version",
        ],
    )

    patcher = uc.Patcher()
    patcher.version_full = LooseVersion(out.decode().split()[1])
    patcher.version_main = patcher.version_full.version[0]
    driver_executable_path = patcher.unzip_package(patcher.fetch_package())
    if not patcher.patch():
        raise AssertionError("Failed to patch chromedriver")

    return driver_executable_path


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
