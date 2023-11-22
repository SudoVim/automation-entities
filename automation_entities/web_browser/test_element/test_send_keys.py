from .common import ElementTestCase
from ...utils import SecretString


class TestSendKeys(ElementTestCase):
    def test_secret(self) -> None:
        val = SecretString("val")
        self.element.send_keys(val)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< send_keys '**********'",
                        }
                    ],
                }
            ]
        )

        self.mock_element.send_keys.assert_called_once_with(val)

    def test_hidden(self) -> None:
        val = "val"
        self.element.send_keys(val, hidden=True)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< send_keys '**********'",
                        }
                    ],
                }
            ]
        )

        self.mock_element.send_keys.assert_called_once_with(val)

    def test_not_hidden(self) -> None:
        val = "val"
        self.element.send_keys(val)

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< send_keys 'val'",
                        }
                    ],
                }
            ]
        )

        self.mock_element.send_keys.assert_called_once_with(val)
