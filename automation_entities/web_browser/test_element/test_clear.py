from .common import ElementTestCase


class TestClear(ElementTestCase):
    def test(self) -> None:
        self.element.clear()

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< clear",
                        }
                    ],
                }
            ]
        )

        self.mock_element.clear.assert_called_once_with()
