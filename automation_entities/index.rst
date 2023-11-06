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

The :class:`entities.Entity` class can also be used toward this end. This class
takes a :class:`context.Context` instance as an argument and provides its own
abstraction on top of it. Generally, this class should be subclassed off of,
but it could theoretically be used on its own. Example of using entities::

    from automation_entities.entities import Entity, describe

    class MyEntity(Entity):

        @describe
        def do_something(self, a, b):
            self.subtask_a(a)
            self.subtask_b(b)

        def subtask_a(self, a):
            with self.interaction():
                self.request(f"subtask_a {a}")
                rsp = some_function(a)

                with self.result() as result:
                    result.log(str(rsp))
                return rsp

        def subtask_b(self, b):
            with self.interaction():
                self.request(f"subtask_b {b}")
                rsp = some_function(b)

                with self.result() as result:
                    result.log(str(rsp))
                return rsp

A call to ``do_something`` could look like::

    MyEntity.do_something(5, "val")
        My Entity:
            <<< subtask_a 5
            >>>
                response a
        My Entity:
            <<< subtask_b val
            >>>
                response b
        Return: None


.. toctree::
    :maxdepth: 1

    context
    entities
    utils
