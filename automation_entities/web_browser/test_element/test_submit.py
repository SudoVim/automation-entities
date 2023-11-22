from .common import ElementTestCase


class TestSubmit(ElementTestCase):
    def test(self) -> None:
        self.element.submit()

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< submit",
                        }
                    ],
                }
            ]
        )

        self.mock_element.submit.assert_called_once_with()
