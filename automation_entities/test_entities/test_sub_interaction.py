import unittest
from unittest.mock import MagicMock, create_autospec
from ..context import Context, Subcontext
from ..entities import Entity, SubInteraction
from ..test_context import ContextTestCase


class BaseTestCase(ContextTestCase):
    entity: Entity

    def setUp(self) -> None:
        super().setUp()

        self.entity = create_autospec(Entity)


class TestInitialize(BaseTestCase):
    def test_no_message(self) -> None:
        sub_interaction = SubInteraction(self.context, self.entity, "delim")
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)
        self.assertEqual(
            self.context.subcontext.return_value, sub_interaction.subcontext
        )

        self.assert_subcontexts(
            [
                {
                    "message": "delim",
                }
            ]
        )

    def test_with_message(self) -> None:
        sub_interaction = SubInteraction(
            self.context, self.entity, "delim", message="interaction message"
        )
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)
        self.assertEqual(
            self.context.subcontext.return_value, sub_interaction.subcontext
        )

        self.assert_subcontexts(
            [
                {
                    "message": "delim interaction message",
                }
            ]
        )


class SubInteractionTestCase(BaseTestCase):
    sub_interaction: SubInteraction
    subcontext: MagicMock

    def setUp(self) -> None:
        super().setUp()

        self.subcontext = create_autospec(Subcontext)
        self.context.subcontext.return_value = self.subcontext
        self.sub_interaction = SubInteraction(self.context, self.entity, "delim")


class TestEnter(SubInteractionTestCase):
    def test_enter(self) -> None:
        cmp_sub_interaction = self.sub_interaction.__enter__()
        self.assertEqual(self.sub_interaction, cmp_sub_interaction)

        self.subcontext.__enter__.assert_called_once_with()


class TestExit(SubInteractionTestCase):
    def test_exit(self) -> None:
        self.sub_interaction.__exit__("a", "b", c="c", d="d")

        self.subcontext.__exit__.assert_called_once_with("a", "b", c="c", d="d")


class TestLog(SubInteractionTestCase):
    def test_log(self) -> None:
        self.sub_interaction.log("log message")

        self.assert_subcontexts(
            [
                {
                    "message": "delim",
                    "log_messages": ["log message"],
                }
            ]
        )
