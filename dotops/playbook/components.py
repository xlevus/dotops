from pathlib import Path
from functools import partial


class Playbook(object):
    ALL = {}

    @classmethod
    def constructor(cls, root: Path):
        return partial(cls, root)

    def __init__(self, root: Path, *tasks):
        self.root = root
        self.tasks = tasks

        if root in self.ALL:
            raise RuntimeError('Only one playbook per file.')

        self.PLAYBOOKS[root] = self

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return "<{}: {}>".format(
            self,
            self.tasks)


class Task(object):
    def __init__(self, module: str, **data):
        self.module = module
        self.data = data

    def __repr__(self):
        return "<{}: {}>".format(self.module, self.data)
