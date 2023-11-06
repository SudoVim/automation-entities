"""
The :mod:`utilities` module contains utilities for the automation_entities
library - namely, the :func:`try_timeout` function.
"""

import time

from typing import Callable, Optional, Tuple, Final, Any, TypeVar

#: default value to display for a :class:`SecretString`
SECRET_STRING_DISPLAY: Final[str] = "'" + ("*" * 10) + "'"


class SecretString(str):
    """
    string that should be displayed as a sequence of asterisks. These will
    not show up in entity logs.
    """

    def __repr__(self) -> str:
        return SECRET_STRING_DISPLAY


#: default timeout value for :func:`try_timeout`
DEFAULT_TIMEOUT: Final[float] = 60.0

#: default step value for :func:`try_timeout`
DEFAULT_STEP: Final[float] = 1.0

#: default step backoff exponent for :func:`try_timeout`
DEFAULT_STEP_EXP: Final[float] = 2.0


class TryAgain(Exception):
    pass


class TimedOut(AssertionError):
    pass


#: default tuple of exceptions to ignore for :func:`try_timeout`
DEFAULT_IGNORE_EXCEPTIONS: Final[Tuple] = (TryAgain,)

R = TypeVar("R")


def try_timeout(
    fcn: Callable[[], R],
    timeout: Optional[float] = None,
    step: Optional[float] = None,
    step_exp: Optional[float] = None,
    ignore_exceptions: Optional[Tuple] = None,
    retry_action: Optional[Callable] = None,
) -> R:
    """
    Try running the given function until a timeout is reached.

        * If the function returns, the return value of the function will be
          returned.
        * If the function raises a :class:`TryAgain` exception, it will be
          retried. Any other exception will be raised up to the calling
          method unless *ignore_exceptions* is specified.
        * If the timeout is reached, a :class:`TimedOut` exception will be
          raised.

    If arguments and keywords are desired in the function call, it's
    recommended to use the :func:`functools.partial` function to generate a
    function that includes the desired args and keywords.

    :param fcn: function to call
    :param float timeout: number of seconds (or a fraction thereof) to
        allow for the function to complete
    :param float step: number of seconds (or a fraction thereof) to wait
        between the first and second calls
    :param float step_exp: exponent to use to calculate the next step for
        exponential backoff of retries (or 1 for no exponential backoff)
    :param tuple ignore_exceptions: subclasses of :class:`Exception` to
        indicate that the function should be retried; if this value is
        specified, :class:`TryAgain` needs to be appended if it's also to
        be used to indicate the action should be retried
    param retry_action: function to call before subsequent retries
    """
    timeout = timeout or DEFAULT_TIMEOUT
    step = step or DEFAULT_STEP
    step_exp = step_exp or DEFAULT_STEP_EXP
    ignore_exceptions = ignore_exceptions or (TryAgain,)
    start_time = time.time()
    while True:
        try:
            return fcn()

        except Exception as e:
            if not isinstance(e, ignore_exceptions):
                raise

            curr_time = time.time()
            if curr_time < start_time or curr_time > start_time + timeout:
                raise TimedOut("timeout reached")

            time.sleep(min(step, (start_time + timeout) - curr_time))
            step *= step_exp
            if retry_action is not None:
                retry_action()
