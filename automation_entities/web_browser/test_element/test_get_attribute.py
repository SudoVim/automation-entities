from .common import ElementTestCase
from unittest.mock import call


class TestGetAttribute(ElementTestCase):
    def test_no_attribute(self) -> None:
        self.mock_element.reset_mock()

        cmp_val = self.element.get_attribute("attr_name")
        self.assertIsNone(cmp_val)

        self.assert_subcontexts(
            [
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
            ]
        )

        self.mock_element.get_attribute.assert_called_once_with("attr_name")

    def test_found_attribute(self) -> None:
        self.attributes["attr_name"] = "attr_val"
        cmp_val = self.element.get_attribute("attr_name")
        self.assertEqual("attr_val", cmp_val)

        self.assert_subcontexts(
            [
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
                }
            ]
        )
