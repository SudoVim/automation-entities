from ...context import Context
from selenium.webdriver.remote.webdriver import WebDriver
from ..web_browser import WebBrowser
from unittest.mock import MagicMock, create_autospec
from ...test_context import ContextTestCase


class WebBrowserTestCase(ContextTestCase):
    driver: MagicMock
    baseurl: str
    web_browser: WebBrowser

    def setUp(self) -> None:
        super().setUp()

        self.driver = create_autospec(WebDriver)
        self.baseurl = "https://example.com"
        self.web_browser = WebBrowser(self.context, self.baseurl)
        self.web_browser._driver = self.driver
