import sys
from functools import wraps

from plumbum import colors as colour
from plumbum.commands.processes import CommandNotFound

from .modules.exec import ModuleNotFound, ModuleExecFailed


class ErrorHandler(object):
    def __init__(self):
        self.handlers = {}

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if type in self.handlers:
            return self.handlers[type](value)

    def add_handler(self, klass, func):
        if klass in self.handlers:
            raise RuntimeError("Handler for '{}' exists".format(klass))
        self.handlers[klass] = func

    def handler(self, klass):
        def _inner(func):
            self.add_handler(klass, func)
            return func
        return _inner

    def decorate(self, func):
        @wraps(func)
        def _inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return _inner


error_handler = ErrorHandler()


@error_handler.handler(CommandNotFound)
def _command_not_found(e):
    command = " ".join(e.program[0])
    print(colour.red | "Could not find the command '{}'.".format(command),
          file=sys.stderr)
    print(colour.yellow | "Searched paths: {}".format(",".join(e.path)))
    exit(127)


@error_handler.handler(ModuleNotFound)
def _module_not_found(e):
    print(colour.red | "Could not find module '{}'.".format(e.module),
          file=sys.stderr)
    exit(1)


@error_handler.handler(ModuleExecFailed)
def _module_exec_failed(e):
    print(colour.red | "Failed to execute module '{}'.".format(e.module),
          file=sys.stderr)
    exit(1)
