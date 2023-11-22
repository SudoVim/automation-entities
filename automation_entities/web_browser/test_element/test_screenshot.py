from .common import ElementTestCase


class TestScreenshot(ElementTestCase):
    def test(self) -> None:
        self.element.screenshot("my/file.png")

        self.assert_subcontexts(
            [
                {
                    "message": "<common />:",
                    "subcontexts": [
                        {
                            "message": "<<< screenshot my/file.png",
                        }
                    ],
                }
            ]
        )

        self.mock_element.screenshot.assert_called_once_with("my/file.png")
