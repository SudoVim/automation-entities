"""
the web browser itself
"""

import functools
from typing import Optional, NamedTuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from ..context import Context

from ..utils import try_timeout, TimedOut
from ..entities import Entity
from .driver import create_webdriver, Browser


class WebBrowser(Entity):
    """
    :class:`Entity` representing a web browser logged into a web page. This can
    be used as a building block to create an :class:`Entity` representing a
    web client.

    :param Context context: the context to give this entity
    :param str baseurl: the base url of the web page
    :param Browser browser: the browser to use
    :param Optional[str] user_data_dir: (optional) where to store user data
    :param bool headless: whether to start the browser in headless mode

    .. automethod:: debug_info
    .. automethod:: close
    .. automethod:: refresh
    """

    baseurl: str
    browser: Browser
    user_data_dir: Optional[str]
    headless: bool

    _driver: Optional[WebDriver]

    class WebBrowserDebugInfo(NamedTuple):
        url: str
        title: str
        name: str
        window: dict

    def __init__(
        self,
        context: Context,
        baseurl: str,
        browser: Browser = "chrome",
        user_data_dir: Optional[str] = None,
        headless: bool = True,
    ):
        self.baseurl = baseurl
        self.browser = browser
        self.user_data_dir = user_data_dir
        self.headless = headless

        self._driver = None

        super().__init__(context, f"WebBrowser {self.baseurl}")

    def debug_info(self) -> WebBrowserDebugInfo:
        """
        Gather and return debug information about the client.
        """
        return self.WebBrowserDebugInfo(
            url=self.driver.current_url,
            title=self.driver.title,
            name=self.driver.name,
            window=self.driver.get_window_rect(),
        )

    @property
    def driver(self) -> WebDriver:
        """
        selenium driver object with which to interface with web client
        """
        if self._driver is None:
            with self.interaction():
                self.request(f"open {self.baseurl}")

                self._driver = create_webdriver(
                    self.browser,
                    headless=self.headless,
                    user_data_dir=self.user_data_dir,
                )

                self._driver.set_page_load_timeout(30)

                # FIXME: This should probably be configurable.
                self._driver.set_window_size(1600, 900)
                self._driver.get(self.baseurl)

        return self._driver

    def close(self) -> None:
        """
        Close the browser.
        """
        with self.interaction():
            self.request("close")
            self.driver.close()
            self._driver = None

    def refresh(self) -> None:
        """
        Refresh the current page.
        """
        with self.interaction():
            self.request("refresh")
            self.driver.refresh()
            self.page_info_result()

    def page_info_result(self) -> None:
        """
        Log page info.
        """
        with self.result() as result:
            result.log(f"Title: {self.driver.title}")

            try:
                h1 = try_timeout(
                    functools.partial(self.driver.find_element, "xpath", "//h1"),
                    ignore_exceptions=(NoSuchElementException,),
                    timeout=2,
                )

            except TimedOut:
                h1 = None

            if h1:
                header = h1.text
                result.log(f"Header: {header}")
