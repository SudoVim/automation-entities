from .common import WebBrowserTestCase


class TestGetElements(WebBrowserTestCase):
    def test_empty(self) -> None:
        elements = self.web_browser.get_elements("//div")
        self.assertEqual([], elements)

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< get_elements //div",
                            "subcontexts": [
                                {
                                    "message": ">>>",
                                    "log_messages": ["--nothing--"],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

        self.driver.find_elements.assert_called_once_with("xpath", "//div")

    def test_with_element(self) -> None:
        e = self.create_element_mock()
        self.driver.find_elements.return_value = [e]

        elements = self.web_browser.get_elements("//div")
        self.assertEqual(1, len(elements))
        self.assertEqual(e, elements[0].element)

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< get_elements //div",
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

        self.driver.find_elements.assert_called_once_with("xpath", "//div")
