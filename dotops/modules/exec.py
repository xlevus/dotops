import os
import sys
import json
import logging
import subprocess
from typing import Iterable, Mapping, Any

from colours import colour

from ..utils import import_string
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
        print(colour.blue("{}: {}".format(self.name, data)))

        try:
            self.exec(data, capture)
        except subprocess.CalledProcessError as e:
            print(colour.red("{} Failed\n".format(self.name)))
            print(colour.red(e.stderr.decode('utf-8')))


if __name__ == '__main__':
    set_log_level()

    module = sys.argv[1]
    data = json.loads(sys.argv[2])

    klass = import_string(module)
    inst = klass()

    logger.debug("Executing '{}' in '{}'".format(
        module, os.getcwd()))

    inst.main(**data)
