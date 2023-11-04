"""
This module pertains to contexts. A context is an object that tracks the current
action.
"""

import os
import json
import collections.abc

import six

class Subcontext(object):
    """
        object denoting a position lower down the context stack; this object
        shouldn't be created directly but should be used by calling
        :meth:`Context.subcontext`

        .. attribute:: context

            :class:`Context` representing the context object this subcontext
            came from

        .. attribute:: log_position

            `int` log position to save for the super context
    """

    def __init__(self, context):
        self.context = context
        self.log_position = None

    def __enter__(self):
        self.log_position = self.context.log_position
        self.context.log_position += 1
        return self

    def __exit__(self, *args, **kwds):
        self.context.log_position = self.log_position

class Context(object):
    """
        The Context is an object that provides a common entrypoint into which
        all information surrounding the current automated routine is sent.

        :param dict config_defaults: default configuration values to give to
            the :attr:`config` object

        .. attribute:: log_position

            ``int`` current subcontext depth

        .. attribute:: config

            :class:`Config` class representing the configuration of the current
                context

        .. automethod:: log
    """

    CONTEXT_DEPTH = 4

    def __init__(self, config_defaults=None):
        self.log_position = 0
        self.config = Config(defaults=config_defaults)

    def log(self, message):
        """
            log given *message* to the context
        """
        spaces = " " * (self.log_position * self.CONTEXT_DEPTH)
        six.print_(f"{spaces}{message}")

    def subcontext(self, message) -> Subcontext:
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
        return Subcontext(self)

    def set_config_file(self, filepath):
        """
            set config file to the given *filepath*
        """
        self.config.set_filepath(filepath)

def patch_dict(original, patch):
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

    def __init__(self, defaults=None):
        self.filepath = None
        self.defaults = defaults
        self._data = {}

        if self.defaults is not None:
            self.patch(self.defaults)

    def patch(self, new_vals):
        """
            patch given original ``dict`` with new values
        """
        patch_dict(self._data, new_vals)

    def set_filepath(self, filepath):
        """
            set persistence filepath to *filepath*
        """
        self.filepath = filepath
        self.load()

    def persist(self):
        """
            persist new config to the file
        """
        with open(self.filepath, 'w') as fobj:
            json.dump(
                self._data,
                fobj,
                sort_keys=True,
                indent=4,
            )

    def load(self):
        """
            load config from file
        """
        if os.path.isfile(self.filepath):
            with open(self.filepath) as fobj:
                self.patch(json.load(fobj))

        self.persist()

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, val):
        self._data.__setitem__(key, val)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return self._data.__len__()

background = Context()
