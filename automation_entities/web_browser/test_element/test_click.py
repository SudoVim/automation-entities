from .common import ElementTestCase


class TestClick(ElementTestCase):
    def test(self) -> None:
        self.element.click()

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< click",
                        }
                    ],
                }
            ]
        )

        self.mock_element.click.assert_called_once_with()
