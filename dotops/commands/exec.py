import os
import sys
import logging
import subprocess

from typing import Iterator, Iterable
from pathlib import Path

from ..context import context
from ..utils import find_executable


logger = logging.getLogger(__name__)


class CommandNotFound(RuntimeError):
    pass


def find_command(command: str) -> str:
    path = find_executable(
        'dotops-' + command,
        additional_roots=[Path(sys.argv[0]).parent])

    if path is None:
        raise CommandNotFound("Unable to find command '{}'".format(command))

    return path


def run_command(command: str, cli_args: Iterable[str]) -> None:
    cmd = [
        find_command(command),
    ] + cli_args

    run = subprocess.run(cmd)
    run.check_returncode()
