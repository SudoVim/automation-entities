from .common import WebBrowserTestCase
from unittest.mock import patch, MagicMock

class TestWaitPage(WebBrowserTestCase):
    @patch('automation_entities.web_browser.web_browser.try_timeout')
    def test_minimal(self, try_timeout: MagicMock) -> None:
        self.web_browser.wait_page("/page")

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< wait_page /page timeout=None baseurl=None",
                        "subcontexts": [{
                            "message": ">>>",
                        }],
                    }],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.web_browser._wait_any_of_pages_fcn,
            args=(('/page',),),
            kwargs={'baseurl': None},
            timeout_kwargs={'timeout': None},
        )

    @patch('automation_entities.web_browser.web_browser.try_timeout')
    def test_with_optional(self, try_timeout: MagicMock) -> None:
        self.web_browser.wait_page("/page", timeout=5.3, baseurl="https://subdomain.example.com")

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< wait_page /page timeout=5.3 baseurl=https://subdomain.example.com",
                        "subcontexts": [{
                            "message": ">>>",
                        }],
                    }],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.web_browser._wait_any_of_pages_fcn,
            args=(('/page',),),
            kwargs={'baseurl': "https://subdomain.example.com"},
            timeout_kwargs={'timeout': 5.3},
        )
