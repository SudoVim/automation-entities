from typing import Any, Dict, Iterator, List, NamedTuple, Optional
from unittest.mock import MagicMock, call, create_autospec

from ..context import Context
from ..test_utils import UtilsTestCase


class ContextTestCase(UtilsTestCase):
    """
    TestCase base class that presents an :attr:`context` and implements a
    :meth:`assert_subcontext` method that can be used to assert that the
    context itself created specific subcontexts.

    .. autoattribute:: context

    .. automethod:: assert_subcontext
    """

    #: mocked context
    context: MagicMock

    def setUp(self) -> None:
        self.context = create_autospec(Context)

    def assert_subcontexts(self, shb: List[Dict]) -> None:
        """
        Assert that the givn *shb* ``dict`` matches the discovered subcontext
        data.
        """
        self.assertEqual(shb, [s.as_dict() for s in self.get_subcontext_comparisons()])

    def get_subcontext_comparisons(self) -> List["SubcontextComparison"]:
        """
        Assert that the givn *shb* ``dict`` matches the discovered subcontext
        data.
        """
        return SubcontextComparison.discover_from_calls(
            self.context.subcontext.mock_calls.__iter__()
        )


class SubcontextComparison(NamedTuple):
    #: The message given to create this subcontext
    message: str
    #: Subcontexts of this subcontext
    subcontexts: List["SubcontextComparison"]
    #: log messages left in this subcontext
    log_messages: List[str]

    @classmethod
    def discover_from_calls(cls, calls: Iterator[Any]) -> List["SubcontextComparison"]:
        """
        Discover a :class:`SubcontextComparison` that can be asserted on from
        the given *calls*.
        """
        ret = []
        for c in calls:
            message = cls.get_log_message(c)
            ret.append(cls.discover_single(message, calls))

        return ret

    @classmethod
    def discover_single(
        cls, message: str, calls: Iterator[Any]
    ) -> "SubcontextComparison":
        """
        Discover a :class:`SubcontextComparison` that can be asserted on from
        the given *calls*.
        """
        self = cls(message=message, subcontexts=[], log_messages=[])
        self.discover_subcontexts(calls)
        return self

    def discover_subcontexts(self, calls: Iterator[Any]) -> None:
        """
        Discover all subcontexts from *calls* and populate this object with
        their data.
        """
        for c in calls:
            if self.is_exit_call(c):
                return

            if self.is_enter_call(c):
                continue

            if self.is_log_call(c):
                self.log_messages.append(self.get_log_message(c))

            if self.is_subcontext_call(c):
                message = self.get_log_message(c)
                self.subcontexts.append(self.discover_single(message, calls))

            # Ignore everything else. These MagicMock calls are pretty noisy,
            # so I'm airing on the side of only discovering things that I care
            # about.

    @staticmethod
    def is_enter_call(c: Any) -> bool:
        """
        Check and return if the given call *c* is a call to __enter__.
        """
        return f"{c}" == "call().__enter__()"

    @staticmethod
    def is_exit_call(c: Any) -> bool:
        """
        Check and return if the given call *c* is a call to __exit__.
        """
        return f"{c}".startswith("call().__exit__(")

    @staticmethod
    def is_log_call(c: Any) -> bool:
        """
        Check and return if the given call *c* is a call to log.
        """
        repr_val = f"{c}"
        return repr_val.startswith("call().log(") or repr_val.startswith(
            "call().__enter__().log("
        )

    @staticmethod
    def is_subcontext_call(c: Any) -> bool:
        """
        Check and return if the given call *c* is a subcontext call.
        """
        repr_val = f"{c}"
        return repr_val.startswith("call('") or repr_val.startswith('call("')

    @staticmethod
    def get_log_message(c: Any) -> str:
        """
        Return a given call's *c* log message.
        """
        if len(c.args) != 1:
            raise AssertionError(f"call {c} has more than one argument")
        return c.args[0]

    def as_dict(self) -> Dict[str, Any]:
        """
        Represent this object as a ``dict``.
        """
        ret: Dict[str, Any] = {"message": self.message}
        if len(self.subcontexts) > 0:
            ret["subcontexts"] = [s.as_dict() for s in self.subcontexts]

        if len(self.log_messages) > 0:
            ret["log_messages"] = self.log_messages

        return ret
