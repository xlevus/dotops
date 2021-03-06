import os
import sys
import json
import logging
import subprocess
from typing import Iterable, Mapping, Any

from plumbum import colors as colour

from ..utils import import_string, indent_string
from ..context import context


logger = logging.getLogger(__name__)

T_Data = Mapping[str, Any]


MODULE_ALIASES = {
    'apply': 'dotops.modules.apply.Apply',
    'zypper': 'dotops.modules.zypper.Zypper',
    'pip': 'dotops.modules.pip.Pip',
}


class ModuleNotFound(Exception):
    def __init__(self, module):
        self.module = module


class ModuleExecFailed(Exception):
    def __init__(self, module, data):
        self.module = module
        self.data = data


class Module(object):
    def __init__(self, name: str):
        self.name = name
        self.root_command = self._load()

    def __repr__(self):
        return "<Module: {}>".format(self.name)

    @classmethod
    def resolve_alias(cls, module: str) -> str:
        if module in MODULE_ALIASES:
            return MODULE_ALIASES[module]
        return module

    def _load(self) -> Iterable[str]:
        module = self.resolve_alias(self.name)

        try:
            import_string(module)
            return [sys.executable,
                    '-m',
                    'dotops.modules._runner',
                    module]
        except ImportError:
            # External modules not implemented.
            pass

        raise ModuleNotFound(self.name)

    def exec(self, data, capture=False) -> None:
        cmd = self.root_command + [
            json.dumps(data)
        ]
        logger.info("Running: {}".format(" ".join(cmd)))

        pipe = subprocess.PIPE if capture else None
        subprocess.run(cmd, check=True, stdout=pipe, stderr=pipe)

    def exec_pretty(self, data, capture=None):
        capture = capture or context.get('capture_output', True)

        print(colour.blue | "{}: {}".format(self.name, data),
              end=" " if capture else None)

        if not capture:
            # Flush output, so failed command's stdout comes below
            # our status line.
            sys.stdout.flush()

        try:
            self.exec(data, capture)
        except subprocess.CalledProcessError as e:
            print(colour.red | colour.bold | "ERROR")

            if capture:
                if e.stdout:
                    stdout = indent_string(
                        e.stdout.decode('utf-8'),
                        indent='O: ')
                    print(colour.yellow | stdout)

                if e.stderr:
                    stderr = indent_string(
                        e.stderr.decode('utf-8'),
                        indent='E: ')
                    print(colour.red | stderr)

            raise ModuleExecFailed(self.name, data)
        else:
            print(colour.green | colour.bold | "OK")
