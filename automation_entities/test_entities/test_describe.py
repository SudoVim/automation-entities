import unittest
from unittest.mock import MagicMock, create_autospec
from ..entities import describe, Entity
from ..context import Context, Subcontext


class MyEntity(Entity):
    def my_func(
        self, a: str, b: str, c: str = "default_c", d: str = "default_d"
    ) -> str:
        return f"{a}, {b}, {c}, {d}"


class TestDescribe(unittest.TestCase):
    entity: MyEntity
    context: MagicMock

    def setUp(self) -> None:
        self.context = create_autospec(Context)
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

        self.context.subcontext.assert_called_once_with("MyEntity.my_func('a', 'b'):")
        self.context.log.assert_called_once_with("Return: 'a, b, default_c, default_d'")

    def test_kwargs(self) -> None:
        inner = describe(MyEntity.my_func)
        cmp_return = inner(self.entity, "a", "b", c="cval", d="dval")

        self.context.subcontext.assert_called_once_with(
            "MyEntity.my_func('a', 'b', c='cval', d='dval'):"
        )
        self.context.log.assert_called_once_with("Return: 'a, b, cval, dval'")

    def test_too_long(self) -> None:
        inner = describe(MyEntity.my_func)
        cmp_return = inner(self.entity, "a" * 60, "b" * 60)

        self.context.subcontext.assert_called_once_with(
            "MyEntity.my_func('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb...):"
        )
        self.context.log.assert_called_once_with(
            "Return: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb..."
        )
