from unittest.mock import MagicMock, call, patch

from .common import WebBrowserTestCase


class TestDownloadFile(WebBrowserTestCase):
    @patch("builtins.open")
    @patch("automation_entities.web_browser.web_browser.requests")
    def test_minimal(self, requests: MagicMock, mock_open: MagicMock) -> None:
        self.driver.current_url = "https://example.com/some/path.html"
        self.driver.execute_script.return_value = "browser user agent"
        self.driver.get_cookies.return_value = [
            {
                "name": "cookie-name",
                "value": "cookie-value",
            }
        ]

        s = requests.session.return_value
        r = s.request.return_value
        r.content = "file-content"

        self.web_browser.download_file("file_url", "destination")

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< download_file file_url -> destination",
                            "subcontexts": [
                                {
                                    "message": "WebBrowser https://example.com:",
                                    "subcontexts": [
                                        {
                                            "message": "<<< request GET file_url",
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                }
            ]
        )

        self.driver.execute_script.assert_called_once_with(
            "return navigator.userAgent;"
        )

        self.assertEqual(call(), requests.session.mock_calls[0])
        self.assertEqual(
            [
                call(
                    {
                        "User-Agent": "browser user agent",
                        "Origin": "https://example.com",
                        "Referer": "https://example.com/some/path.html",
                    }
                ),
                call({}),
            ],
            s.headers.update.mock_calls,
        )

        s.cookies.update.assert_called_once_with(
            {
                "cookie-name": "cookie-value",
            }
        )

        s.request.assert_called_once_with(
            "GET", "https://example.com/file_url", allow_redirects=True
        )

        mock_open.assert_called_once_with("destination", "wb")

        fobj = mock_open.return_value.__enter__.return_value
        fobj.write.assert_called_once_with("file-content")
