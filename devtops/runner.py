import os
import sys
import json
import logging
import subprocess

from pathlib import PurePath

from .context import context

logger = logging.getLogger(__name__)


ROOT_CMD = 'devtop'

CORE_MODULES = {
}


class ModuleNotFound(Exception):
    pass


def run_module(module, *, cli_args=None, data=None):
    if (cli_args is not None and data is not None) or \
       (cli_args is None and data is None):
        raise RuntimeError("You must provide one of 'args' or 'data'.")

    if module in CORE_MODULES:
        return run_core(module, cli_args=cli_args, data=data)
    else:
        return run_external(module, cli_args=cli_args, data=data)


def run_core(module, *, cli_args=None, data=None):
    mod = CORE_MODULES[module]

    if args:
        return mod.cli(cli_args)

    else:
        return mod.main(*data)


def find_external(module):
    command = '{}-{}'.format(ROOT_CMD, module)

    search_paths = [
        '{}/modules'.format(context.root),
        PurePath(sys.argv[0]).parent,
    ] + os.get_exec_path()

    for path in search_paths:
        path = PurePath(path) / command
        logger.debug("Looking for file '{}'".format(path))
        if os.path.exists(path):
            return str(path)

    raise ModuleNotFound("Unable to find executable '{}'.".format(command))


def run_external(module, *, cli_args=None, data=None):
    cmd = [find_external(module)]

    if cli_args:
        cmd += cli_args

    else:
        cmd += ['--json', json.dumps(data)]

    try:
        run = subprocess.run(cmd)
        run.check_returncode()
    except FileNotFoundError:
        raise ModuleNotFound("Command '{}' could not be found.".format(cmd[0]))
