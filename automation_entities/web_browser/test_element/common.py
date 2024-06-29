from typing import Dict
from unittest.mock import MagicMock, create_autospec

from selenium.webdriver.remote.webelement import WebElement

from ...context import Context
from ...test_context import ContextTestCase
from ..web_browser import Element


class ElementTestCase(ContextTestCase):
    mock_element: MagicMock
    element: Element
    attributes: Dict[str, str]

    def setUp(self) -> None:
        super().setUp()

        self.attributes = {}
        self.mock_element = create_autospec(WebElement)
        self.mock_element.tag_name = "common"
        self.mock_element.text = ""
        self.mock_element.get_attribute.side_effect = lambda key: self.attributes.get(
            key
        )

        self.element = Element(self.context, self.mock_element)

    def create_element_mock(self):
        ret = create_autospec(WebElement)
        ret.tag_name = "element"
        ret.text = ""
        ret.get_attribute.return_value = None

        return ret
