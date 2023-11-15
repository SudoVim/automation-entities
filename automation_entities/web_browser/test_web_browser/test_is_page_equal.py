from .common import WebBrowserTestCase

class TestIsPageEqual(WebBrowserTestCase):
    def test_not_equal(self) -> None:
        self.driver.current_url = "https://subdomain.example.com/page"

        self.assertFalse(self.web_browser.is_page_equal("/page"))

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< is_page_equal /page baseurl=None",
                        "subcontexts": [{
                            "message": ">>>",
                            "log_messages": [
                                "URL: https://subdomain.example.com/page",
                            ],
                        }],
                    }],
                }
            ]
        )

    def test_equal(self) -> None:
        self.driver.current_url = "https://example.com/page"

        self.assertTrue(self.web_browser.is_page_equal("/page"))

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< is_page_equal /page baseurl=None",
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

    def test_equal_baseurl(self) -> None:
        self.driver.current_url = "https://subdomain.example.com/page"

        self.assertTrue(self.web_browser.is_page_equal("/page", baseurl="https://subdomain.example.com"))

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [{
                        "message": "<<< is_page_equal /page baseurl=https://subdomain.example.com",
                        "subcontexts": [{
                            "message": ">>>",
                            "log_messages": [
                                "URL: https://subdomain.example.com/page",
                            ],
                        }],
                    }],
                }
            ]
        )

