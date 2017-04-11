import logging

from pathlib import Path
from functools import partial
from collections import OrderedDict

from plumbum import local

from ..modules.exec import Module

logger = logging.getLogger(__name__)


class Playbook(object):
    ALL = OrderedDict()

    @classmethod
    def constructor(cls, root: Path):
        """
        The `Playbook` will require an identifier. The user could
        pass this into the object, but that's not really ideal.

        Instead, we'll pass the curried constructor with the path
        of the playbook as `playbook` into the lisp-globals.

        Also means, no macros.
        """
        return partial(cls, root)

    def __init__(self, root: Path, *tasks):
        self.root = root
        self.tasks = tasks

        if root in self.ALL:
            raise RuntimeError('Only one playbook per file.')

        # Record a record of the playbook. This saves us writing macros to
        # populate the modules global namespace with something we can look for
        # again later.
        self.ALL[root] = self

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return "<{}: {}>".format(
            self,
            self.tasks)

    def execute(self):
        logger.debug("Executing playbook {}".format(self))

        with local.cwd(self.root):
            for i, task in enumerate(self.tasks):

                # Filter out 'tasks' that are None.
                # This should allow you to write playbooks that wrap tasks
                # with (if x (task ...)) easily.
                if task is None:
                    logger.debug("Skipping task #{} as it is None".format(i))
                    continue

                task.execute()


class Task(object):
    def __init__(self, module: str, *options, **data):
        self.module = Module(module)
        self.data = data

        self.options = {
            'name': None,
            'depends': [],
        }

        if len(options) == 1:
            self.options.update(options[0])

    def __repr__(self):
        return "<{}: {}>".format(self.module, self.data)

    def execute(self):
        self.module.exec_pretty(self.data)
