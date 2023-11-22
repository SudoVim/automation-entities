"""
the web browser itself
"""

import functools
import urllib.parse
from typing import Optional, NamedTuple, Union, Tuple, List

from assertpy import assert_that
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)

from ..context import Context

from ..utils import try_timeout, TimedOut, Timeout, TryAgain, SecretString
from ..entities import Entity, SubInteraction, describe
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
    .. automethod:: wait_not_page
    .. automethod:: wait_none_of_pages
    .. automethod:: get_elements
    .. automethod:: get_element
    .. automethod:: get_element_retry
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

    def wait_not_page(
        self, page: str, timeout: Timeout = None, baseurl: Optional[str] = None
    ) -> None:
        """
        Wait until we are no longer on the given *page*.
        """
        with self.interaction():
            self.request(f"wait_not_page {page} timeout={timeout} baseurl={baseurl}")
            self._wait_none_of_pages((page,), timeout=timeout, baseurl=baseurl)

    def wait_none_of_pages(
        self,
        pages: Tuple[str, ...],
        timeout: Timeout = None,
        baseurl: Optional[str] = None,
    ) -> None:
        """
        Wait until we are no longer on any of the given *pages*.
        """
        with self.interaction():
            self.request(
                f"wait_none_of_pages {pages} timeout={timeout} baseurl={baseurl}"
            )
            self._wait_none_of_pages(pages, timeout=timeout, baseurl=baseurl)

    def _wait_none_of_pages(
        self,
        pages: Tuple[str, ...],
        timeout: Timeout = None,
        baseurl: Optional[str] = None,
    ) -> None:
        with self.result() as result:
            try_timeout(
                functools.partial(
                    self._wait_none_of_pages_fcn, result, pages, baseurl=baseurl
                ),
                timeout=timeout,
            )

    def _wait_none_of_pages_fcn(
        self,
        result: SubInteraction,
        pages: Tuple[str, ...],
        baseurl: Optional[str] = None,
    ) -> None:
        if any(self.compare_page(result, p, baseurl=baseurl) for p in pages):
            raise TryAgain

    def get_elements(self, xpath: str) -> List["Element"]:
        """
        Get and return all elements matching given *xpath*.
        """
        with self.interaction():
            self.request(f"get_elements {xpath}")
            elements = [
                Element(self.context, e)
                for e in self.driver.find_elements("xpath", xpath)
            ]

            with self.result() as result:
                if len(elements) == 0:
                    result.log("--nothing--")

                else:
                    for element in elements:
                        result.log(f"{element}")

                return elements

    def get_element(self, xpath: str) -> "Element":
        """
        Get and return elements matching given *xpath*.
        """
        with self.interaction():
            self.request(f"get_element {xpath}")
            e = self.driver.find_element("xpath", xpath)

            with self.result() as result:
                element = Element(self.context, e)
                result.log(f"{element}")
                return element

    @describe
    def get_element_retry(self, xpath: str, timeout: Timeout = None) -> "Element":
        """
        Query the element denoted by the given *xpath* until it's discovered or
        the given *timeout* is reached.
        """
        return try_timeout(
            functools.partial(self.get_element, xpath),
            ignore_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
            ),
            timeout=timeout,
        )


class Element(Entity):
    """
    :class:`Entity` wrapping the
    :class:`selenium.webdriver.remote.webelement.WebElement` component.

    .. autoattribute:: element

    .. automethod:: get_elements
    .. automethod:: get_element
    .. automethod:: get_element_retry
    .. automethod:: get_attribute
    .. automethod:: assert_attribute
    .. automethod:: clear
    .. automethod:: send_keys
    .. automethod:: screenshot
    .. automethod:: submit
    .. automethod:: click
    """

    #: selenium element to wrap
    element: WebElement

    def __init__(self, context, element):
        self.element = element

        super().__init__(context, f"{self}")

    def get_elements(self, xpath: str) -> List["Element"]:
        """
        Get and return all elements matching given *xpath*.
        """
        with self.interaction():
            self.request(f"get_elements {xpath}")

            elements = [
                Element(self.context, e)
                for e in self.element.find_elements("xpath", xpath)
            ]

            with self.result() as result:
                if len(elements) == 0:
                    result.log("--nothing--")

                else:
                    for element in elements:
                        result.log(f"{element}")

                return elements

    def get_element(self, xpath: str) -> "Element":
        """
        get an elements matching given xpath
        """
        with self.interaction():
            self.request(f"get_element {xpath}")

            e = self.element.find_element("xpath", xpath)

            with self.result() as result:
                element = Element(self.context, e)
                result.log(f"{element}")
                return element

    @describe
    def get_element_retry(self, xpath: str, timeout: Timeout = None) -> "Element":
        """
        continually query the given element until success
        """
        return try_timeout(
            functools.partial(self.get_element, xpath),
            ignore_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
            ),
            timeout=timeout,
        )

    def get_attribute(self, attr: str) -> Optional[str]:
        """
        Return the attribute denoted by the given *attr* string.
        """
        with self.interaction():
            self.request(f"get_attribute {attr}")
            with self.result() as result:
                val = self.element.get_attribute(attr)
                result.log(f"{val}")
                return val

    @describe
    def assert_attribute(self, attr: str, val: str) -> None:
        """
        Assert that the given *attr* is the given *val*.
        """
        assert_that(self.get_attribute(attr)).is_equal_to(val)

    def clear(self) -> None:
        """
        Clear the text in this element. This should be used for elements that
        take user input.
        """
        with self.interaction():
            self.request(f"clear")
            self.element.clear()

    def send_keys(self, keys: str, hidden: bool = False) -> None:
        """
        Send the given *keys* to the element and optionally hide them from
        logging with the *hidden* keyword argument. This should be used for
        elements that take user input.
        """
        hidden = hidden or isinstance(keys, SecretString)
        keys = keys if not hidden else SecretString(keys)
        print_val = repr(keys)
        with self.interaction():
            self.request(f"send_keys {print_val}")
            self.element.send_keys(keys)

    def screenshot(self, fname: str) -> None:
        """
        Take a screenshot of the given element and save it to *fname*.
        """
        with self.interaction():
            self.request(f"screenshot {fname}")
            self.element.screenshot(fname)

    def submit(self) -> None:
        """
        Submit the given element. This should be used for form elements.
        """
        with self.interaction():
            self.request("submit")
            self.element.submit()

    def click(self) -> None:
        """
        Click the given element.
        """
        with self.interaction():
            self.request("click")
            self.element.click()

    PRINT_ATTRS = ["name", "placeholder", "value"]

    def __str__(self) -> str:
        print_attrs = {}
        for attr in self.PRINT_ATTRS:
            val = self.element.get_attribute(attr)
            if val:
                print_attrs[attr] = val

        def format_attrs():
            if not print_attrs:
                return ""

            return " " + (
                " ".join(f"{k}={repr(v)}" for k, v in sorted(print_attrs.items()))
            )

        text = self.element.text
        if len(text) > 100:
            text = text[:97] + "..."
        if self.element.text:
            return f"<{self.element.tag_name}{format_attrs()}>{text}</{self.element.tag_name}>"

        else:
            return f"<{self.element.tag_name}{format_attrs()} />"

    def __repr__(self) -> str:
        return self.__str__()
