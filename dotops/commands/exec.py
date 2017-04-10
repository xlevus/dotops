import os
import sys
import logging
import subprocess

from typing import Iterator, Iterable
from pathlib import Path

from ..context import context


logger = logging.getLogger(__name__)


class CommandNotFound(RuntimeError):
    pass


class CommandNotExecutable(RuntimeError):
    pass


def command_search_paths(command) -> Iterator[str]:
    yield Path(context.root) / 'plugins' / command / 'command'

    exec_name = 'dotops-' + command
    yield Path(sys.argv[0]).parent / exec_name

    for path in os.get_exec_path():
        yield Path(path) / exec_name


def find_command(command: str) -> str:
    for path in command_search_paths(command):
        if path.exists():
            logger.debug("Found '{}'".format(path))
            if not os.access(path, os.X_OK):
                raise CommandNotExecutable(
                    "Command '{}' needs execution permissions".format(command))
            return str(path)
    raise CommandNotFound("Unable to find command '{}'".format(command))


def run_command(command: str, cli_args: Iterable[str]) -> None:
    cmd = [
        find_command(command),
    ] + cli_args

    run = subprocess.run(cmd)
    run.check_returncode()
