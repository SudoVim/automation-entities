from unittest.mock import MagicMock, patch

from ...utils import TimedOut
from .common import WebBrowserTestCase


class TestRefresh(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_refresh(self, try_timeout_mock: MagicMock) -> None:
        self.driver.title = "Personal Home Page"
        try_timeout_mock.side_effect = TimedOut

        self.web_browser.refresh()

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< refresh",
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

        self.driver.refresh.assert_called_once_with()
