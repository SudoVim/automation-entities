from unittest.mock import patch, MagicMock, create_autospec
from .common import WebBrowserTestCase
from ...utils import TimedOut
from selenium.webdriver.remote.webelement import WebElement


class TestPageInfoResult(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_no_header(self, try_timeout_mock: MagicMock) -> None:
        self.driver.title = "Personal Home Page"
        try_timeout_mock.side_effect = TimedOut

        self.web_browser.page_info_result()

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "Title: Personal Home Page",
                    ],
                }
            ]
        )

    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test_with_header(self, try_timeout_mock: MagicMock) -> None:
        self.driver.title = "Personal Home Page"

        mock_element = create_autospec(WebElement)
        mock_element.text = "My Home"
        try_timeout_mock.return_value = mock_element

        self.web_browser.page_info_result()

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                    "log_messages": [
                        "Title: Personal Home Page",
                        "Header: My Home",
                    ],
                }
            ]
        )
