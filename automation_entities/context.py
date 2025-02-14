"""
The :mod:`automation_entities.context` module is primarily concerned with the
:class:`Context` class. It contains the basic configuration and logging logic
that will be expanded upon in the higher up :class:`entities.Entity` class.
"""

import collections.abc
import json
import os
import typing


class Subcontext:
    """
    object denoting a position lower down the context stack; this object
    shouldn't be created directly but should be used by calling
    :meth:`Context.subcontext`

    .. autoattribute:: context
    .. autoattribute:: log_position
    """

    #: the parent context
    context: "Context"

    #: the log position to save for the parent context
    log_position: typing.Optional[int]

    already_entered: bool

    def __init__(self, context: "Context"):
        self.context = context
        self.log_position = None
        self.already_entered = False

    def log(self, msg: str) -> None:
        """
        Log given *msg* as a result of an interaction with this subcontext.
        """
        assert (
            self.log_position is not None
        ), "log must only be called in conjunction with __enter__"
        self.context.log(msg)

    def __enter__(self) -> "Subcontext":
        assert not self.already_entered, "a subcontext may only be entered once"

        self.log_position = self.context.log_position
        self.already_entered = True
        self.context.log_position += 1
        return self

    def __exit__(self, *args, **kwds) -> None:
        assert (
            self.log_position is not None
        ), "__exit__ must only be called in conjunction with __enter__"

        self.context.log_position = self.log_position
        self.log_position = None


class Context:
    """
    The Context is an object that provides a common entrypoint into which
    all information surrounding the current automated routine is sent.

    :param dict config_defaults: default configuration values to give to
        the :attr:`config` object

    .. autoattribute:: CONTEXT_DEPTH

    .. autoattribute:: log_position
    .. autoattribute:: config

    .. automethod:: log
    .. automethod:: subcontext
    .. automethod:: set_config_file
    """

    #: the number of spaces to use when logging from this context
    CONTEXT_DEPTH: int = 4

    #: the current log position
    log_position: int

    subcontext_class: typing.Type["Subcontext"]

    #: the configuration represented by this context
    config: "Config"

    def __init__(
        self,
        config_defaults: typing.Optional[dict] = None,
        subcontext_class: typing.Optional[typing.Type["Subcontext"]] = None,
    ) -> None:
        self.log_position = 0
        self.subcontext_class = subcontext_class or Subcontext
        self.config = Config(defaults=config_defaults)

    def log(self, message: str) -> None:
        """
        log given *message* to the context
        """
        spaces = " " * (self.log_position * self.CONTEXT_DEPTH)
        print(f"{spaces}{message}")

    def subcontext(self, message: str) -> Subcontext:
        """
        Log the given *message* to create a new subcontext. This method
        returns a context manager that will increment the
        :attr:`log_position` on *__enter__* and decrement it back on
        *__exit__*::

            >>> with ctx.subcontext("sub context"):
            ...     ctx.log("subcontext message")
            ...
            sub context
                subcontext message

        :rtype: Subcontext
        :returns: subcontext object
        """
        self.log(message)
        return self.subcontext_class(self)

    def set_config_file(self, filepath: str) -> None:
        """
        set config file to the given *filepath*
        """
        self.config.set_filepath(filepath)


def patch_dict(original: dict, patch: dict) -> None:
    """
    Patch given *original* dict with the new *patch*. This function
    recursively iterates over all keys in the patch and applies them to
    existing keys in the original. It does not replace a sub-dict. Rather,
    it recursively replaces its keys.
    """
    for k, v in patch.items():
        if k not in original or not isinstance(v, dict):
            original[k] = v
        elif isinstance(v, dict):
            patch_dict(original[k], v)


class Config(collections.abc.MutableMapping):
    """
    The Config object represents the configuration of the current context.
    It's used as a ``dict`` object and can be instantiated with default
    values. If the :meth:`set_filepath` method is called, the :meth:`load`
    and :meth:`persist` methods can be used to load configuration data from
    the filepath and persist it to the filepath, respectively.

    .. attribute:: filepath

        ``str`` filepath containing the configuration

    .. automethod:: patch
    .. automethod:: set_filepath
    .. automethod:: persist
    .. automethod:: load
    """

    filepath: typing.Optional[str]
    defaults: typing.Optional[dict]
    _data: dict

    def __init__(self, defaults: typing.Optional[dict] = None):
        self.filepath = None
        self.defaults = defaults
        self._data = {}

        if self.defaults is not None:
            self.patch(self.defaults)

    def patch(self, new_vals: dict) -> None:
        """
        patch given original ``dict`` with new values
        """
        patch_dict(self._data, new_vals)

    def set_filepath(self, filepath: str) -> None:
        """
        set persistence filepath to *filepath*
        """
        self.filepath = filepath
        self.load()

    def persist(self) -> None:
        """
        persist new config to the file
        """
        assert self.filepath is not None, "filepath must be set before calling persist"

        with open(self.filepath, "w") as fobj:
            json.dump(
                self._data,
                fobj,
                sort_keys=True,
                indent=4,
            )

    def load(self) -> None:
        """
        load config from file
        """
        assert self.filepath is not None, "filepath must be set before calling load"

        if os.path.isfile(self.filepath):
            with open(self.filepath) as fobj:
                self.patch(json.load(fobj))

        self.persist()

    def __getitem__(self, key: typing.Any) -> typing.Any:
        return self._data.__getitem__(key)

    def __setitem__(self, key: typing.Any, val: typing.Any) -> None:
        self._data.__setitem__(key, val)

    def __delitem__(self, key: typing.Any) -> None:
        self._data.__delitem__(key)

    def __iter__(self) -> typing.Iterator:
        return self._data.__iter__()

    def __len__(self) -> int:
        return self._data.__len__()


background = Context()
