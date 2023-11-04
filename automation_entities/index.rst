.. _automation_entities:

.. module:: automation_entities

===================
Automation Entities
===================

The main point of entry of this module is through the :class:`context.Context`
class. This class provides a common point of entry for all log messages::

    >>> from automation_entities.context import Context
    >>> ctx = Context()
    >>> ctx.log("message")
    message
    >>> with ctx.subcontext("sub context"):
    ...     ctx.log("subcontext message")
    ...
    sub context
        subcontext message

In this way, an output trail can be described such that it's clear what's being
called and what's calling what else.
