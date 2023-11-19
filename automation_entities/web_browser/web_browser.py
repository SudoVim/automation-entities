"""
the web browser itself
"""

import functools
import urllib.parse
from typing import Optional, NamedTuple, Union, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..context import Context

from ..utils import try_timeout, TimedOut, Timeout, TryAgain
from ..entities import Entity, SubInteraction
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

    .. automethod:: get
    .. automethod:: is_page_equal
    .. automethod:: check_page
    .. automethod:: wait_page
    .. automethod:: wait_any_of_pages
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

    def get(self, url: str) -> None:
        """
        Navigate to the given *url*.
        """
        with self.interaction():
            self.request(f"GET {url}")
            try_timeout(
                functools.partial(self.driver.get, url),
                ignore_exceptions=(TimeoutException,),
            )
            self.page_info_result()

    def compare_page(
        self, result: SubInteraction, page: str, baseurl: Optional[str] = None
    ) -> bool:
        """
        Compare that the current page matches the given *page* and, optionally,
        *baseurl*.
        """
        compare_page = urllib.parse.urlparse((baseurl or self.baseurl) + page)
        current_url = self.driver.current_url
        is_page = urllib.parse.urlparse(current_url)
        result.log(f"URL: {current_url}")
        if compare_page.scheme != is_page.scheme:
            return False
        if compare_page.netloc != is_page.netloc:
            return False
        if compare_page.path.rstrip("/") != is_page.path.rstrip("/"):
            return False
        # TODO: I'd like for this function to eventually allow comparisons of
        # other components of the URL, but for now, I'm keeping it simple.
        return True

    def is_page_equal(self, page: str, baseurl: Optional[str] = None) -> bool:
        """
        Check if the current URL patches the given *page*.
        """
        with self.interaction():
            self.request(f"is_page_equal {page} baseurl={baseurl}")
            with self.result() as result:
                return self.compare_page(result, page, baseurl=baseurl)

    def check_page(self) -> str:
        """
        Return the current page URL and ensure that it's logged.
        """
        with self.interaction():
            self.request(f"check_page")
            with self.result() as result:
                result.log(f"URL: {self.driver.current_url}")
                return self.driver.current_url

    def wait_page(self, page: str, timeout: Timeout = None, baseurl=None):
        """
        wait until we get to the desired page
        """
        with self.interaction():
            self.request(f"wait_page {page} timeout={timeout} baseurl={baseurl}")

            self._wait_any_of_pages((page,), timeout=timeout, baseurl=baseurl)

    def wait_any_of_pages(
        self,
        pages: Tuple[str, ...],
        timeout: Timeout = None,
        baseurl: Optional[str] = None,
    ) -> None:
        """
        Wait until any of the given *pages* are reached.
        """
        with self.interaction():
            self.request(
                f"wait_any_of_pages {pages} timeout={timeout} baseurl={baseurl}"
            )

            self._wait_any_of_pages(pages, timeout=timeout, baseurl=baseurl)

    def _wait_any_of_pages(
        self,
        pages: Tuple[str, ...],
        timeout: Timeout = None,
        baseurl: Optional[str] = None,
    ) -> None:
        with self.result() as result:
            try_timeout(
                functools.partial(
                    self._wait_any_of_pages_fcn, result, pages, baseurl=baseurl
                ),
                timeout=timeout,
            )

    def _wait_any_of_pages_fcn(
        self,
        result: SubInteraction,
        pages: Tuple[str, ...],
        baseurl: Optional[str] = None,
    ) -> None:
        if not any(self.compare_page(result, p, baseurl=baseurl) for p in pages):
            raise TryAgain
