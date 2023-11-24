from .common import WebBrowserTestCase
from unittest.mock import patch, MagicMock, call


class TestClick(WebBrowserTestCase):
    @patch("automation_entities.web_browser.web_browser.ActionChains")
    def test_minimal(self, ActionChains: MagicMock) -> None:
        self.web_browser.click()

        self.assert_subcontexts(
            [
                {
                    "message": "WebBrowser https://example.com:",
                    "subcontexts": [
                        {
                            "message": "<<< click",
                        }
                    ],
                }
            ]
        )

        self.assertEqual(3, len(ActionChains.mock_calls))
        self.assertEqual(call(self.driver), ActionChains.mock_calls[0])
        self.assertEqual(
            call(),
            ActionChains.return_value.click.mock_calls[0],
        )
        self.assertEqual(
            call(),
            ActionChains.return_value.click.return_value.perform.mock_calls[0],
        )
