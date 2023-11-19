import unittest
from unittest.mock import MagicMock, create_autospec, call
from ..context import Context
from typing import List, NamedTuple, Iterator, Optional, Dict, Any, Callable, Tuple
from assertpy import assert_that


class UtilsTestCase(unittest.TestCase):
    def assert_try_timeout_partial(
        self,
        c: Any,
        fcn: Callable,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[Any, Any]] = None,
        timeout_kwargs: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """
        Assert that the given call is a "try_timeout" call with the given
        parameters.
        """
        partial = c.args[0]
        self.assertEqual(fcn, partial.func)
        self.assertEqual(args or tuple(), partial.args)
        self.assertEqual(kwargs or {}, partial.keywords)
        self.assertEqual(timeout_kwargs or {}, c.kwargs)
