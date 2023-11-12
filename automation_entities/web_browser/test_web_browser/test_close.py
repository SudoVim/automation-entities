from .common import WebBrowserTestCase


class TestClose(WebBrowserTestCase):
    def test_close(self) -> None:
        self.web_browser.close()

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< close",
                        }
                    ],
                }
            ]
        )

        self.driver.close.assert_called_once_with()
