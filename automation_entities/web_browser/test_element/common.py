from ...context import Context
from selenium.webdriver.remote.webelement import WebElement
from ..web_browser import Element
from unittest.mock import MagicMock, create_autospec
from ...test_context import ContextTestCase


class ElementTestCase(ContextTestCase):
    mock_element: MagicMock
    element: Element

    def setUp(self) -> None:
        super().setUp()

        self.mock_element = create_autospec(WebElement)
        self.element = Element(self.context, self.mock_element)
