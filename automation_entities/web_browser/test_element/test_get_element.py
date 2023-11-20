from .common import ElementTestCase


class TestGetElement(ElementTestCase):
    def test(self) -> None:
        e = self.create_element_mock()
        self.mock_element.find_element.return_value = e

        element = self.element.get_element("//div")
        self.assertEqual(e, element.element)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
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

        self.mock_element.find_element.assert_called_once_with("xpath", "//div")
