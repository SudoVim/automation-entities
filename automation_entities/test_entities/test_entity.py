import unittest
from unittest.mock import MagicMock, create_autospec, patch
from ..context import Context
from ..entities import Entity


class BaseTestCase(unittest.TestCase):
    context: MagicMock
    entity: Entity

    def setUp(self) -> None:
        self.context = create_autospec(Context)
        self.entity = Entity(self.context, "MyEntity")


class TestInteraction(BaseTestCase):
    def test_interaction(self) -> None:
        self.entity.interaction()

        self.context.subcontext.assert_called_once_with("MyEntity:")


class TestRequest(BaseTestCase):
    def test_no_message(self) -> None:
        sub_interaction = self.entity.request()
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.context.subcontext.assert_called_once_with("<<<")

    def test_with_message(self) -> None:
        sub_interaction = self.entity.request("request message")
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.context.subcontext.assert_called_once_with("<<< request message")


class TestResult(BaseTestCase):
    def test_no_message(self) -> None:
        sub_interaction = self.entity.result()
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.context.subcontext.assert_called_once_with(">>>")

    def test_with_message(self) -> None:
        sub_interaction = self.entity.result("result message")
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.context.subcontext.assert_called_once_with(">>> result message")


class TestSleep(BaseTestCase):
    @patch("time.sleep")
    def test_sleep(self, mock_sleep: MagicMock) -> None:
        self.entity.sleep(5.3)

        self.context.subcontext.assert_any_call("MyEntity:")
        self.context.subcontext.assert_any_call("<<< sleep 5.3")
        mock_sleep.assert_called_once_with(5.3)
