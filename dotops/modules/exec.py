import os
import sys
import json
import logging
import subprocess

from typing import Mapping, Any

from ..utils import import_string
from ..cli import set_log_level


logger = logging.getLogger(__name__)

T_Data = Mapping[str, Any]


MODULE_ALIASES = {
    'apply': 'dotops.modules.apply.Apply',
    'zypper': 'dotops.modules.packages.Zypper',
    'pip': 'dotops.modules.pip.Pip',
}


class ModuleNotFound(RuntimeError):
    pass


def resolve_alias(module: str) -> str:
    if module in MODULE_ALIASES:
        return MODULE_ALIASES[module]
    return module


def exec_module(module: str, data: T_Data) -> None:
    module = resolve_alias(module)

    try:
        import_string(module)
        exec_python(module, data)
    except ImportError:
        exec_external(module, data)


def exec_python(module: str, data: T_Data) -> None:
    """
    Executes python module in a subprocess.
    """
    cmd = [
        sys.executable,
        '-m',
        __name__,
        module,
        json.dumps(data)
    ]
    run = subprocess.run(cmd)
    run.check_returncode()


def exec_external(module: str, data: T_Data) -> None:
    # TODO: Implement 'external' modules.
    # Unsure of what naming convention they should follow.
    # `my.module.dotop` ?
    raise NotImplementedError()


if __name__ == '__main__':
    set_log_level()

    module = sys.argv[1]
    data = json.loads(sys.argv[2])

    klass = import_string(module)
    inst = klass()

    logger.debug("Executing '{}' in '{}'".format(
        module, os.getcwd()))

    inst.main(**data)
