from .common import ElementTestCase


class TestGetElements(ElementTestCase):
    def test_empty(self) -> None:
        elements = self.element.get_elements("//div")
        self.assertEqual([], elements)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
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

        self.mock_element.find_elements.assert_called_once_with("xpath", "//div")

    def test_with_element(self) -> None:
        e = self.create_element_mock()
        self.mock_element.find_elements.return_value = [e]

        elements = self.element.get_elements("//div")
        self.assertEqual(1, len(elements))
        self.assertEqual(e, elements[0].element)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
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

        self.mock_element.find_elements.assert_called_once_with("xpath", "//div")
