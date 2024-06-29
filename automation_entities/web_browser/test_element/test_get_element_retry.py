from unittest.mock import MagicMock, patch

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from ..web_browser import Element
from .common import ElementTestCase


class TestGetElementRetry(ElementTestCase):
    @patch("automation_entities.web_browser.web_browser.try_timeout")
    def test(self, try_timeout: MagicMock) -> None:
        element = Element(self.context, self.create_element_mock())
        try_timeout.return_value = element

        cmp_element = self.element.get_element_retry("//div")
        self.assertEqual(element, cmp_element)

        self.assert_subcontexts(
            [
                {
                    "message": "Element.get_element_retry('//div'):",
                    "log_messages": ["Return: <element />"],
                }
            ]
        )

        self.assertEqual(1, len(try_timeout.mock_calls))
        self.assert_try_timeout_partial(
            try_timeout.mock_calls[0],
            self.element.get_element,
            args=("//div",),
            timeout_kwargs={
                "ignore_exceptions": (
                    NoSuchElementException,
                    StaleElementReferenceException,
                ),
                "timeout": None,
            },
        )
