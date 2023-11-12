import unittest
from unittest.mock import create_autospec

from ..context import Context, Subcontext


class SubcontextTest(unittest.TestCase):
    context: Context

    def setUp(self) -> None:
        self.context = Context()

    def test_initialize(self) -> None:
        subcontext = Subcontext(self.context)
        self.assertEqual(self.context, subcontext.context)
        self.assertIsNone(subcontext.log_position)

    def test_log_not_entered(self) -> None:
        subcontext = Subcontext(self.context)
        with self.assertRaisesRegex(
            AssertionError, "log must only be called in conjunction with __enter__"
        ):
            subcontext.log("log message")

    def test_log_entered(self) -> None:
        mock_context = create_autospec(Context)

        subcontext = Subcontext(mock_context)
        subcontext.log_position = 1
        subcontext.log("log message")

        mock_context.log.assert_called_once_with("log message")

    def test_enter(self) -> None:
        subcontext = Subcontext(self.context)
        cmp_subcontext = subcontext.__enter__()
        self.assertEqual(subcontext, cmp_subcontext)

        self.assertEqual(0, subcontext.log_position)
        self.assertTrue(subcontext.already_entered)
        self.assertEqual(1, self.context.log_position)

    def test_cannot_reenter(self) -> None:
        subcontext = Subcontext(self.context)
        subcontext.already_entered = True
        with self.assertRaisesRegex(
            AssertionError, "a subcontext may only be entered once"
        ):
            cmp_subcontext = subcontext.__enter__()

    def test_exit_none_log_position(self) -> None:
        subcontext = Subcontext(self.context)
        with self.assertRaisesRegex(
            AssertionError, "__exit__ must only be called in conjunction with __enter__"
        ):
            subcontext.__exit__()

    def test_exit(self) -> None:
        subcontext = Subcontext(self.context)
        subcontext.__enter__()
        subcontext.__exit__()

        self.assertIsNone(subcontext.log_position)
        self.assertEqual(0, self.context.log_position)
