import logging
import argparse
from typing import Union

from .context import context
from .commands.exec import run_command


parser = argparse.ArgumentParser()

parser.add_argument('--root', metavar='PATH', default='~/.dotops')
parser.add_argument('--logging', metavar='LEVEL', default=None)

parser.add_argument('command', nargs='?', default='help')
parser.add_argument('args', nargs=argparse.REMAINDER)


def set_log_level(level: Union[None, str] = None) -> None:
    """Sets the log level on the default logger and current context.
    If no level is specified, level is inferred from context.
    """
    if level is None:
        try:
            level = context.logging
        except AttributeError:
            level = 'CRITICAL'
    else:
        context.logging = level

    logging.basicConfig(level=level)


def cli():
    args = parser.parse_args()

    context.root = context.get('root', args.root)
    set_log_level(args.logging)

    run_command(args.command, cli_args=args.args)
