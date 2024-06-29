from unittest.mock import MagicMock, call, patch

from .common import WebBrowserTestCase


class TestMoveTo(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.ActionChains")
    def test_minimal(self, ActionChains: MagicMock) -> None:
        self.web_browser.move_to(self.element)

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< move_to <common />",
                        }
                    ],
                }
            ]
        )

        self.assertEqual(3, len(ActionChains.mock_calls))
        self.assertEqual(call(self.driver), ActionChains.mock_calls[0])
        self.assertEqual(
            call(self.mock_element),
            ActionChains.return_value.move_to_element.mock_calls[0],
        )
        self.assertEqual(
            call(),
            ActionChains.return_value.move_to_element.return_value.perform.mock_calls[
                0
            ],
        )
