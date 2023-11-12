from .common import WebBrowserTestCase


class TestDebugInfo(WebBrowserTestCase):
    def test_debug_info(self) -> None:
        self.driver.current_url = "current_url"
        self.driver.title = "title"
        self.driver.name = "name"
        self.driver.get_window_rect.return_value = {"window": "rect"}
        cmp_debug_info = self.web_browser.debug_info()
        self.assertEqual(
            {
                "url": "current_url",
                "title": "title",
                "name": "name",
                "window": {"window": "rect"},
            },
            cmp_debug_info._asdict(),
        )
