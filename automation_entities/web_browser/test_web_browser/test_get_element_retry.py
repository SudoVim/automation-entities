from unittest.mock import patch, MagicMock
from .common import WebBrowserTestCase
from ..web_browser import Element
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)


class TestGetElementRetry(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test(self, try_timeout: MagicMock) -> None:
        element = Element(self.context, self.create_element_mock())
        try_timeout.return_value = element

        cmp_element = self.web_browser.get_element_retry("//div")
        self.assertEqual(element, cmp_element)

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser.get_element_retry('//div'):",
                    "log_messages": ["Return: <element />"],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.web_browser.get_element,
            args=("//div",),
            timeout_kwargs={
                "ignore_exceptions": (
                    NoSuchElementException,
                    StaleElementReferenceException,
                ),
                "timeout": None,
            },
        )
