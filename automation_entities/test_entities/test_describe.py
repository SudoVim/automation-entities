from unittest.mock import MagicMock, create_autospec

from ..context import Context, Subcontext
from ..entities import Entity, describe
from ..test_context import ContextTestCase


class MyEntity(Entity):
    def my_func(
        self, a: str, b: str, c: str = "default_c", d: str = "default_d"
    ) -> str:
        return f"{a}, {b}, {c}, {d}"


class TestDescribe(ContextTestCase):
    entity: MyEntity

    def setUp(self) -> None:
        super().setUp()

        self.entity = MyEntity(self.context, "MyEntityName")

    def test_not_entity(self) -> None:
        inner = describe(MyEntity.my_func)
        with self.assertRaisesRegex(
            AssertionError, "received invalid 'self' value type"
        ):
            inner("invalid", "a", "b")

    def test_simple(self) -> None:
        inner = describe(MyEntity.my_func)
        cmp_return = inner(self.entity, "a", "b")
        self.assertEqual("a, b, default_c, default_d", cmp_return)

        self.assert_subcontexts(
            [
                {
                    "message": "MyEntity.my_func('a', 'b'):",
                    "log_messages": ["Return: 'a, b, default_c, default_d'"],
                }
            ]
        )

    def test_kwargs(self) -> None:
        inner = describe(MyEntity.my_func)
        cmp_return = inner(self.entity, "a", "b", c="cval", d="dval")

        self.assert_subcontexts(
            [
                {
                    "message": "MyEntity.my_func('a', 'b', c='cval', d='dval'):",
                    "log_messages": ["Return: 'a, b, cval, dval'"],
                }
            ]
        )

    def test_too_long(self) -> None:
        inner = describe(MyEntity.my_func)
        cmp_return = inner(self.entity, "a" * 60, "b" * 60)

        self.assert_subcontexts(
            [
                {
                    "message": "MyEntity.my_func('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb...):",
                    "log_messages": [
                        "Return: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb..."
                    ],
                }
            ]
        )
