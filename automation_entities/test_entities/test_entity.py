from unittest.mock import MagicMock, patch

from ..entities import Entity
from ..test_context import ContextTestCase


class BaseTestCase(ContextTestCase):
    entity: Entity

    def setUp(self) -> None:
        super().setUp()

        self.entity = Entity(self.context, "MyEntity")


class TestInteraction(BaseTestCase):
    def test_interaction(self) -> None:
        self.entity.interaction()

        self.assert_subcontexts(
            [
                {
                    "message": "MyEntity:",
                }
            ]
        )


class TestRequest(BaseTestCase):
    def test_no_message(self) -> None:
        sub_interaction = self.entity.request()
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.assert_subcontexts(
            [
                {
                    "message": "<<<",
                }
            ]
        )

    def test_with_message(self) -> None:
        sub_interaction = self.entity.request("request message")
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.assert_subcontexts(
            [
                {
                    "message": "<<< request message",
                }
            ]
        )


class TestResult(BaseTestCase):
    def test_no_message(self) -> None:
        sub_interaction = self.entity.result()
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.assert_subcontexts(
            [
                {
                    "message": ">>>",
                }
            ]
        )

    def test_with_message(self) -> None:
        sub_interaction = self.entity.result("result message")
        self.assertEqual(self.context, sub_interaction.context)
        self.assertEqual(self.entity, sub_interaction.entity)

        self.assert_subcontexts(
            [
                {
                    "message": ">>> result message",
                }
            ]
        )


class TestSleep(BaseTestCase):
    @patch("time.sleep")
    def test_sleep(self, mock_sleep: MagicMock) -> None:
        self.entity.sleep(5.3)

        self.assert_subcontexts(
            [
                {
                    "message": "MyEntity:",
                    "subcontexts": [
                        {
                            "message": "<<< sleep 5.3",
                        }
                    ],
                }
            ]
        )

        mock_sleep.assert_called_once_with(5.3)
