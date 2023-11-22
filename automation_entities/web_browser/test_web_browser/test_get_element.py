from .common import WebBrowserTestCase


class TestGetElement(WebBrowserTestCase):
    def test(self) -> None:
        e = self.create_element_mock()
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
                                    "log_messages": ["<element />"],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.driver.find_element.assert_called_once_with("xpath", "//div")
