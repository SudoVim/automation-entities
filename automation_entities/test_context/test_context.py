import unittest
from unittest.mock import patch, MagicMock

from ..context import Context


class InitializeTest(unittest.TestCase):
    def test_no_defaults(self) -> None:
        context = Context()
        self.assertEqual(0, context.log_position)
        self.assertIsNone(context.config.defaults)

    def test_with_defaults(self) -> None:
        context = Context(config_defaults={"key": "val"})
        self.assertEqual(0, context.log_position)
        self.assertEqual({"key": "val"}, context.config.defaults)


class ContextTestCase(unittest.TestCase):
    context: Context

    def setUp(self) -> None:
        self.context = Context()


class LogTest(ContextTestCase):
    @patch("builtins.print")
    def test_zero_depth(self, mock_print: MagicMock) -> None:
        self.context.log("log message")
        mock_print.assert_called_with("log message")

    @patch("builtins.print")
    def test_nonzero_depth(self, mock_print: MagicMock) -> None:
        self.context.log_position = 1

        self.context.log("log message")
        mock_print.assert_called_with("    log message")


class SubcontextTest(ContextTestCase):
    @patch("builtins.print")
    def test_subcontext(self, mock_print: MagicMock) -> None:
        cmp_subcontext = self.context.subcontext("log message")
        mock_print.assert_called_with("log message")

        self.assertEqual(self.context, cmp_subcontext.context)


class SetConfigFileTest(ContextTestCase):
    @patch("builtins.open")
    @patch("os.path")
    def test_set_config_file(self, mock_path: MagicMock, mock_open: MagicMock) -> None:
        mock_path.is_file.return_value = True

        mock_fobj = MagicMock()
        mock_open.return_value = mock_fobj
        mock_fobj.__enter__.return_value = mock_fobj
        mock_fobj.read.return_value = '{"key":"val"}'

        self.context.set_config_file("config/filepath.json")

        self.assertEqual("config/filepath.json", self.context.config.filepath)
