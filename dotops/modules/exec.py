import os
import sys
import json
import logging
import subprocess
from typing import Iterable, Mapping, Any

from plumbum import colors as colour

from ..utils import import_string, indent_string
from ..cli import set_log_level


logger = logging.getLogger(__name__)

T_Data = Mapping[str, Any]


MODULE_ALIASES = {
    'apply': 'dotops.modules.apply.Apply',
    'zypper': 'dotops.modules.zypper.Zypper',
    'pip': 'dotops.modules.pip.Pip',
}


class ModuleNotFound(RuntimeError):
    pass


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
                    __name__,
                    module]
        except ImportError:
            # External modules not implemented.
            pass

        raise ModuleNotFound("Unable to find module '{}'.".format(self.name))

    def exec(self, data, capture=False) -> None:

        cmd = self.root_command + [
            json.dumps(data)
        ]
        logger.info("Running: {}".format(" ".join(cmd)))

        pipe = subprocess.PIPE if capture else None
        subprocess.run(cmd, check=True, stdout=pipe, stderr=pipe)

    def exec_pretty(self, data, capture=True):
        print(colour.blue | "{}: {}".format(self.name, data), end=" ")

        try:
            self.exec(data, capture)
        except subprocess.CalledProcessError as e:
            print(colour.red | colour.bold | "ERROR")

            if capture:
                stderr = indent_string(
                    e.stderr.decode('utf-8'),
                    indent='E: ')
                print(colour.red | stderr)
        else:
            print(colour.green | colour.bold | "OK")


if __name__ == '__main__':
    set_log_level()

    module = sys.argv[1]
    data = json.loads(sys.argv[2])

    klass = import_string(module)
    inst = klass()

    logger.debug("Executing '{}' in '{}'".format(
        module, os.getcwd()))

    inst.main(**data)
