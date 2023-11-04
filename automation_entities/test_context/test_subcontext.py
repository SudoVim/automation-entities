import unittest

from ..context import Context, Subcontext


class SubcontextTest(unittest.TestCase):
    context: Context

    def setUp(self) -> None:
        self.context = Context()

    def test_initialize(self) -> None:
        subcontext = Subcontext(self.context)
        self.assertEqual(self.context, subcontext.context)
        self.assertIsNone(subcontext.log_position)

    def test_enter(self) -> None:
        subcontext = Subcontext(self.context)
        cmp_subcontext = subcontext.__enter__()
        self.assertEqual(subcontext, cmp_subcontext)

        self.assertEqual(0, subcontext.log_position)
        self.assertEqual(1, self.context.log_position)

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
