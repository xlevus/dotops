import os
import sys
import imp
import logging
from typing import Iterable

from pathlib import Path

from hy.importer import import_file_to_ast, ast_compile
from hy.compiler import HyTypeError
from hy.lex import LexException

from .components import Playbook, Task


logger = logging.getLogger(__name__)

DEFAULT_MACROS = ""


class PlaybookNotFound(RuntimeError):
    pass


def _globals(root, module):
    module.__dict__['playbook'] = Playbook.constructor(root)
    module.__dict__['task'] = Task
    return module.__dict__


def find_playbook(root: Path) -> Path:
    filenames = ['playbook', 'playbook.hy']

    for filename in filenames:
        path = root / filename
        if path.exists():
            return path
    raise RuntimeError('No playbook(.hy) found.')


def load_playbook(root: Path) -> None:
    """Import content from fpath and puts it into a Python module.
    Returns the module."""
    module_name = 'dotops.playbooks.' + root.name
    fpath = find_playbook(root)

    try:
        _ast = import_file_to_ast(fpath, module_name)
        mod = imp.new_module(module_name)

        mod.__file__ = fpath
        eval(ast_compile(_ast, fpath, "exec"), _globals(root, mod))
    except (HyTypeError, LexException) as e:
        if e.source is None:
            with open(fpath, 'rt') as fp:
                e.source = fp.read()
            e.filename = fpath
        raise
    except Exception:
        sys.modules.pop(module_name, None)
        raise


def exec_playbook(path):
    path = path.resolve()

    orig_path = Path.cwd()
    os.chdir(path)

    playbook = path / 'playbook.hy'
    if not playbook.exists():
        raise PlaybookNotFound("Unable to find playbook in '{}'.".format(
            playbook))

    try:
        logger.debug("Executing playbook in '{}'.".format(path))

        module = load_playbook(playbook)
        _exec(module)

    finally:
        os.chdir(orig_path)


def exec_playbooks(playbooks: Iterable[Path]):
    for root in playbooks:
        load_playbook(root)
