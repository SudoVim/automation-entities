"""
An entity is something that can be interacted with. This abstraction will be
used as a way to log interactions with remote components.
"""

import time
import functools

from typing import Callable, Any, Optional

from .context import Context, Subcontext

def describe(fcn: Callable) -> Callable:
    """
        Decorator for :class:`Entity` instance methods that will describe the
        method call to the entity's context on entrance and print its return
        value on exit.
    """
    @functools.wraps(fcn)
    def inner(self: 'Entity', *args, **kwds) -> Any:
        assert isinstance(self, Entity), "received invalid 'self' value type"

        arg_toks = [repr(a) for a in args] + \
            [f"{k}={repr(v)}" for k, v in kwds.items()]
        arg_str = ", ".join(arg_toks)
        if len(arg_str) > 100:
            arg_str = arg_str[:97] + '...'
        with self.context.subcontext(f"{fcn.__qualname__}({arg_str}):"):
            ret = fcn(self, *args, **kwds)
            ret_str = repr(ret)
            if len(ret_str) > 100:
                ret_str = ret_str[:97] + '...'
            self.context.log(f"Return: {ret_str}")
            return ret

    return inner

class SubInteraction(object):
    """
        Context manager that surrounds a sub-interaction of an entity. This
        class shouldn't be instantiated on its own but should instead be
        returned by calling :meth:`Entity.request` or :meth:`Entity.result`.

        .. automethod:: log
    """

    context: Context
    entity: 'Entity'

    def __init__(self, context: Context, entity: 'Entity', delimeter: str, message: Optional[str] = None):
        self.context = context
        self.entity = entity

        text = delimeter
        if message:
            text += f" {message}"

        self.subcontext = self.context.subcontext(text)

    def __enter__(self) -> 'SubInteraction':
        self.subcontext.__enter__()
        return self

    def __exit__(self, *args, **kwds) -> None:
        self.subcontext.__exit__(*args, **kwds)

    def log(self, msg: str) -> None:
        """
            log given *msg* as a result of an interaction with an entity
        """
        self.context.log(f"{msg}")

class Entity(object):
    """
        This class serves as a base for any object who's purpose is to interact
        with an entity for automation purposes. With this class, any interaction
        with the entity can be described in such a way where the automated
        routine can be debugged after the fact without the need to reproduce it.

        :param Context context: context to associate with this entity
        :param str name: name of this entity to use in logging

        .. autoattribute:: context
        .. autoattribute:: name

        .. automethod:: interaction
        .. automethod:: request
        .. automethod:: result
        .. automethod:: sleep
    """

    #: object representing the relevant context for this entity
    context: Context

    #: name of the entity
    name: str

    def __init__(self, context: Context, name: str):
        self.context = context
        self.name = name

    def interaction(self) -> 'Subcontext':
        """
            log an interaction with the entity; can be used as a context manager
            or not
        """
        return self.context.subcontext(f"{self.name}:")

    def request(self, msg: Optional[str] = None) -> 'SubInteraction':
        """
            log an interaction request; use as a context manager to
            return a :class:`SubInteraction` instance
        """
        return SubInteraction(self.context, self, "<<<", message=msg)

    def result(self, msg: Optional[str] = None) -> 'SubInteraction':
        """
            log the result of an interaction; use as a context manager to
            return a :class:`SubInteraction` instance
        """
        return SubInteraction(self.context, self, ">>>", message=msg)

    def sleep(self, sleep_time: float) -> None:
        """
            Sleep for the given *sleep_time* amount of seconds.
        """
        with self.interaction():
            self.request(f"sleep {sleep_time}")
            time.sleep(sleep_time)
