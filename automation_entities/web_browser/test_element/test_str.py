from .common import ElementTestCase


class TestStr(ElementTestCase):
    def test_minimal(self) -> None:
        cmp_str = self.element.__str__()
        self.assertEqual("<common />", cmp_str)

    def test_text(self) -> None:
        self.mock_element.text = "Element Text"
        cmp_str = self.element.__str__()
        self.assertEqual("<common>Element Text</common>", cmp_str)

    def test_attributes_no_text(self) -> None:
        self.attributes["name"] = "name"
        self.attributes["placeholder"] = "placeholder"
        self.attributes["value"] = "value"
        cmp_str = self.element.__str__()
        self.assertEqual(
            "<common name='name' placeholder='placeholder' value='value' />", cmp_str
        )

    def test_attributes_with_text(self) -> None:
        self.mock_element.text = "Element Text"
        self.attributes["name"] = "name"
        self.attributes["placeholder"] = "placeholder"
        self.attributes["value"] = "value"
        cmp_str = self.element.__str__()
        self.assertEqual(
            "<common name='name' placeholder='placeholder' value='value'>Element Text</common>",
            cmp_str,
        )

    def test_attributes_under_length(self) -> None:
        self.mock_element.text = "a" * 100
        self.attributes["name"] = "name"
        self.attributes["placeholder"] = "placeholder"
        self.attributes["value"] = "value"
        cmp_str = self.element.__str__()
        self.assertEqual(
            "<common name='name' placeholder='placeholder' value='value'>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</common>",
            cmp_str,
        )

    def test_attributes_over_length(self) -> None:
        self.mock_element.text = "a" * 101
        self.attributes["name"] = "name"
        self.attributes["placeholder"] = "placeholder"
        self.attributes["value"] = "value"
        cmp_str = self.element.__str__()
        self.assertEqual(
            "<common name='name' placeholder='placeholder' value='value'>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...</common>",
            cmp_str,
        )
