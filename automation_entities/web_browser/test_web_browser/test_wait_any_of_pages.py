from unittest.mock import MagicMock, patch

from ...utils import TryAgain
from .common import WebBrowserTestCase


class TestWaitAnyOfPages(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_minimal(self, try_timeout: MagicMock) -> None:
        self.web_browser.wait_any_of_pages(("/page1", "/page2"))

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< wait_any_of_pages ('/page1', '/page2') timeout=None baseurl=None",
                            "subcontexts": [
                                {
                                    "message": ">>>",
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.web_browser._wait_any_of_pages_fcn,
            args=(
                try_timeout.mock_calls[0].args[0].args[0],
                (
                    "/page1",
                    "/page2",
                ),
            ),
            kwargs={"baseurl": None},
            timeout_kwargs={"timeout": None},
        )

    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_with_optional(self, try_timeout: MagicMock) -> None:
        self.web_browser.wait_any_of_pages(
            ("/page1", "/page2"), timeout=5.3, baseurl="https://subdomain.example.com"
        )

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< wait_any_of_pages ('/page1', '/page2') timeout=5.3 baseurl=https://subdomain.example.com",
                            "subcontexts": [
                                {
                                    "message": ">>>",
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.web_browser._wait_any_of_pages_fcn,
            args=(
                try_timeout.mock_calls[0].args[0].args[0],
                (
                    "/page1",
                    "/page2",
                ),
            ),
            kwargs={"baseurl": "https://subdomain.example.com"},
            timeout_kwargs={"timeout": 5.3},
        )

    def test_fcn_no_match(self) -> None:
        self.driver.current_url = "https://example.com/page"

        with self.web_browser.result() as result:
            with self.assertRaises(TryAgain):
                self.web_browser._wait_any_of_pages_fcn(result, ("/page1", "/page2"))

    def test_fcn_matches(self) -> None:
        self.driver.current_url = "https://example.com/page"

        with self.web_browser.result() as result:
            self.web_browser._wait_any_of_pages_fcn(result, ("/page",))

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "URL: https://example.com/page",
                    ],
                }
            ]
        )

    def test_fcn_matches_baseurl(self) -> None:
        self.driver.current_url = "https://subdomain.example.com/page"

        with self.web_browser.result() as result:
            self.web_browser._wait_any_of_pages_fcn(
                result, ("/page",), baseurl="https://subdomain.example.com"
            )

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "URL: https://subdomain.example.com/page",
                    ],
                }
            ]
        )
