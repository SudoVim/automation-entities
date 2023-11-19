from .common import WebBrowserTestCase


class TestComparePage(WebBrowserTestCase):
    def test_wrong_scheme(self) -> None:
        self.driver.current_url = "http://example.com/page"

        with self.web_browser.result() as result:
            self.assertFalse(self.web_browser.compare_page(result, "/page"))

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "URL: http://example.com/page",
                    ],
                }
            ]
        )

    def test_wrong_netloc(self) -> None:
        self.driver.current_url = "https://subdomain.example.com/page"

        with self.web_browser.result() as result:
            self.assertFalse(self.web_browser.compare_page(result, "/page"))

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

    def test_wrong_path(self) -> None:
        self.driver.current_url = "https://example.com/wrong"

        with self.web_browser.result() as result:
            self.assertFalse(self.web_browser.compare_page(result, "/page"))

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "URL: https://example.com/wrong",
                    ],
                }
            ]
        )

    def test_success(self) -> None:
        self.driver.current_url = "https://example.com/page"

        with self.web_browser.result() as result:
            self.assertTrue(self.web_browser.compare_page(result, "/page"))

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

    def test_trim_trailing_current_url(self) -> None:
        self.driver.current_url = "https://example.com/page/"

        with self.web_browser.result() as result:
            self.assertTrue(self.web_browser.compare_page(result, "/page"))

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "URL: https://example.com/page/",
                    ],
                }
            ]
        )

    def test_trim_trailing_path(self) -> None:
        self.driver.current_url = "https://example.com/page"

        with self.web_browser.result() as result:
            self.assertTrue(self.web_browser.compare_page(result, "/page/"))

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

    def test_success_baseurl(self) -> None:
        self.driver.current_url = "https://subdomain.example.com/page"

        with self.web_browser.result() as result:
            self.assertTrue(
                self.web_browser.compare_page(
                    result, "/page", baseurl="https://subdomain.example.com"
                )
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
