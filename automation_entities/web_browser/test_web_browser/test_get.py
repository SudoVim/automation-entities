from unittest.mock import patch, MagicMock
from .common import WebBrowserTestCase
from ...utils import TimedOut
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestGet(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_get(self, try_timeout: MagicMock) -> None:
        self.driver.title = "Personal Home Page"
        try_timeout.side_effect = [None, TimedOut]

        self.web_browser.get("https://some.site.example.com")

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< GET https://some.site.example.com",
                            "subcontexts": [
                                {
                                    "message": ">>>",
                                    "log_messages": [
                                        "Title: Personal Home Page",
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.assertEqual(2, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.driver.get,
            args=("https://some.site.example.com",),
            timeout_kwargs={"ignore_exceptions": (TimeoutException,)},
        )
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[1],
            self.driver.find_element,
            args=("xpath", "//h1"),
            timeout_kwargs={
                "ignore_exceptions": (NoSuchElementException,),
                "timeout": 2,
            },
        )
