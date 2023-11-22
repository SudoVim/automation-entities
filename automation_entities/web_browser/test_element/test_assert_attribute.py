from .common import ElementTestCase


class TestAssertAttribute(ElementTestCase):
    def test_no_attribute(self) -> None:
        with self.assertRaises(AssertionError):
            self.element.assert_attribute("attr_name", "attr_val")

        self.assert_subcontexts(
            [
                {
                    "message": "Element.assert_attribute('attr_name', 'attr_val'):",
                    "subcontexts": [
                        {
                            "message": "<common />:",
                            "subcontexts": [
                                {
                                    "message": "<<< get_attribute attr_name",
                                    "subcontexts": [
                                        {
                                            "message": ">>>",
                                            "log_messages": ["None"],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

    def test_miscompare(self) -> None:
        self.attributes["attr_name"] = "other_val"
        with self.assertRaises(AssertionError):
            self.element.assert_attribute("attr_name", "attr_val")

        self.assert_subcontexts(
            [
                {
                    "message": "Element.assert_attribute('attr_name', 'attr_val'):",
                    "subcontexts": [
                        {
                            "message": "<common />:",
                            "subcontexts": [
                                {
                                    "message": "<<< get_attribute attr_name",
                                    "subcontexts": [
                                        {
                                            "message": ">>>",
                                            "log_messages": ["other_val"],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        )

    def test_success(self) -> None:
        self.attributes["attr_name"] = "attr_val"
        self.element.assert_attribute("attr_name", "attr_val")

        self.assert_subcontexts(
            [
                {
                    "message": "Element.assert_attribute('attr_name', 'attr_val'):",
                    "subcontexts": [
                        {
                            "message": "<common />:",
                            "subcontexts": [
                                {
                                    "message": "<<< get_attribute attr_name",
                                    "subcontexts": [
                                        {
                                            "message": ">>>",
                                            "log_messages": ["attr_val"],
                                        }
                                    ],
                                }
                            ],
                            "log_messages": ["Return: None"],
                        }
                    ],
                }
            ]
        )
