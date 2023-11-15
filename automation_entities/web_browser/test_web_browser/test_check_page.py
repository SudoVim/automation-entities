from .common import WebBrowserTestCase

class TestCheckPage(WebBrowserTestCase):
    def test_not_equal(self) -> None:
        self.driver.current_url = "https://example.com/page"

        self.assertEqual("https://example.com/page", self.web_browser.check_page())

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< check_page",
                        "subcontexts": [{
                            "message": ">>>",
                            "log_messages": [
                                "URL: https://example.com/page",
                            ],
                        }],
                    }],
                }
            ]
        )
