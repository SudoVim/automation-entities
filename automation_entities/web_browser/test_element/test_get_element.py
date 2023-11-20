from unittest.mock import create_autospec
from .common import ElementTestCase
from selenium.webdriver.remote.webelement import WebElement


class TestGetElement(ElementTestCase):
    def test(self) -> None:
        e = create_autospec(WebElement)
        self.mock_element.find_element.return_value = e

        element = self.element.get_element("//div")
        self.assertEqual(e, element.element)

        self.assert_subcontexts(
            [
                {
                    "message": "Element:",
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

        self.mock_element.find_element.assert_called_once_with("xpath", "//div")
