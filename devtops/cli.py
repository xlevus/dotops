import logging
import argparse
import os
import pathlib

from .runner import run_module
from .context import context


parser = argparse.ArgumentParser()
parser.add_argument('--root', metavar='PATH', default='~/.devtop')
parser.add_argument('--logging', metavar='LEVEL', default='CRITICAL')

parser.add_argument('command', nargs='?', default='')
parser.add_argument('args', nargs=argparse.REMAINDER)


def cli():
    args = parser.parse_args()

    context.root = context.get('root', args.root)
    context.logging = context.get('logging', args.logging).upper()
    logging.basicConfig(level=context.logging)

    run_module(args.command, cli_args=args.args)
