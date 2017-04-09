import os
import sys
import json
import logging
from typing import Iterable, Mapping, Any
import subprocess

from pathlib import PurePath

from .context import context
from .utils import import_string

logger = logging.getLogger(__name__)


ROOT_CMD = 'devtop'

CORE_MODULES = {
    'apply': 'devtops.modules.apply.Apply',
    'zypper': 'devtops.modules.packages.Zypper',
    'pip': 'devtops.modules.pip.Pip',
}

T_CliArgs = Iterable[str]
T_DataArgs = Mapping[str, Any]


class ModuleNotFound(Exception):
    pass


def exec_module(module: str, *,
                cli_args: T_CliArgs = None,
                data: T_DataArgs=None):
    """Execute `module` with the given `cli_args` or `data`."""

    if module in CORE_MODULES or '.' in module:
        return exec_core(module, cli_args=cli_args, data=data)

    return exec_external(module, cli_args=cli_args, data=data)


def exec_python(module: str, *,
                cli_args: T_CliArgs = None,
                data: T_DataArgs=None):
    """Execute a native python module."""
    klass = None

    if module in CORE_MODULES:
        module = CORE_MODULES[module]

    try:
        klass = import_string(module)
        instance = klass()
        logger.debug("Using class '{}'.".format(module))
    except ImportError:
        raise ModuleNotFound("Cannot import '{}'.".format(module))

    if cli_args is not None:
        return instance.cli(cli_args)
    else:
        return instance.main(*data)


def external_search_paths() -> Iterable[str]:
    """
    Returns a list of paths to search for external modules.
    """
    search_paths = [
        '{}/modules'.format(context.root),
        PurePath(sys.argv[0]).parent,
    ] + os.get_exec_path()



def find_external(module: str) -> str:
    """
    """
    command = '{}-{}'.format(ROOT_CMD, module)

    for path in search_paths:
        path = PurePath(path) / command
        logger.debug("Looking for file '{}'".format(path))
        if os.path.exists(path):
            logger.info("Found external module '{}'.".format(path))
            return str(path)

    raise ModuleNotFound("Unable to find executable '{}'.".format(command)) # really long


def exec_external(module: str, *,
                cli_args: T_CliArgs = None,
                data: T_DataArgs=None):
    cmd = [find_external(module)]

    if cli_args is not None:
        cmd += cli_args

    else:
        cmd += [json.dumps(data)]

    try:
        run = subprocess.run(cmd)
        run.check_returncode()
    except FileNotFoundError:
        raise ModuleNotFound("Command '{}' could not be found.".format(cmd[0]))
