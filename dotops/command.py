import argparse

from dotops.cli import set_log_level
from dotops.context import context
from dotops.commands.exec import run_command


parser = argparse.ArgumentParser()
parser.add_argument('--root', metavar='PATH', default='~/.dotops')
parser.add_argument('--logging', metavar='LEVEL', default=None)
parser.add_argument('command', nargs='?', default='help')
parser.add_argument('args', nargs=argparse.REMAINDER)


def main():
    args = parser.parse_args()

    context.root = context.get('root', args.root)
    set_log_level(args.logging)

    run_command(args.command, cli_args=args.args)
