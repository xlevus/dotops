import os
import sys
import json
import subprocess

from pathlib import PurePath
from typing import Iterable, Mapping, Any

from ..context import context
from ..utils import import_string


T_Data = Mapping[str, Any]


MODULE_ALIASES = {
    'apply': 'devtops.modules.apply.Apply',
    'zypper': 'devtops.modules.packages.Zypper',
    'pip': 'devtops.modules.pip.Pip',
}


class ModuleNotFound(RuntimeError):
    pass


def resolve_alias(module: str) -> str:
    if module in MODULE_ALIASES:
        return MODULE_ALIASES[module]
    return module


def exec_module(module: str, data: T_Data):
    module = resolve_alias(module)

    try:
        import_string(module)
        return exec_python(module, data)
    except ImportError:
        return exec_external(module, data)


def exec_python(module: str, data: T_Data):
    cmd = [
        sys.executable,
        __file__,
        module,
        json.dumps(data)
    ]
    run = subprocess.run(cmd)
    run.check_returncode()


def exec_external(module: str, data: T_Data):
    raise NotImplementedError()


if __name__ == '__main__':
    try:
        module = sys.argv[1]
        data = json.loads(sys.argv[2])

        klass = import_string(module)
        inst = klass()

        inst.main(**data)
        exit(0)
    except Exception as e:
        exit(1)
