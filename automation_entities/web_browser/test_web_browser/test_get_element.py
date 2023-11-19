from unittest.mock import create_autospec
from .common import WebBrowserTestCase
from selenium.webdriver.remote.webelement import WebElement


class TestGetElement(WebBrowserTestCase):
    def test(self) -> None:
        e = create_autospec(WebElement)
        self.driver.find_element.return_value = e

        element = self.web_browser.get_element("//div")
        self.assertEqual(e, element.element)

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< get_element //div",
                            "subcontexts": [
                                {
                                    "message": ">>>",
                                    "log_messages": ["Element"],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.driver.find_element.assert_called_once_with('xpath', '//div')
