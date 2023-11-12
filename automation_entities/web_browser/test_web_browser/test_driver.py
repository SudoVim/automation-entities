from .common import WebBrowserTestCase
from unittest.mock import patch, MagicMock


class TestDriver(WebBrowserTestCase):
    def test_driver_exists(self) -> None:
        self.web_browser.driver

        self.assert_subcontexts([])

    @patch("automation_entities.web_browser.web_browser.create_webdriver")
    def test_driver_none(self, mock_create_webdriver: MagicMock) -> None:
        self.web_browser._driver = None
        mock_create_webdriver.return_value = self.driver

        self.web_browser.driver

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< open https://example.com",
                        }
                    ],
                }
            ]
        )

        mock_create_webdriver.assert_called_once_with(
            "chrome", headless=True, user_data_dir=None
        )

        self.driver.set_page_load_timeout.assert_called_once_with(30)
        self.driver.set_window_size.assert_called_once_with(1600, 900)
        self.driver.get.assert_called_once_with("https://example.com")

    @patch("automation_entities.web_browser.web_browser.create_webdriver")
    def test_driver_none_optional_args(self, mock_create_webdriver: MagicMock) -> None:
        self.web_browser._driver = None
        self.web_browser.headless = False
        self.web_browser.user_data_dir = "/user/data/dir"
        mock_create_webdriver.return_value = self.driver

        self.web_browser.driver

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< open https://example.com",
                        }
                    ],
                }
            ]
        )

        mock_create_webdriver.assert_called_once_with(
            "chrome", headless=False, user_data_dir="/user/data/dir"
        )
