import os
import sys
import imp
import logging

from pathlib import Path

from hy.importer import import_buffer_to_ast, ast_compile
from hy.compiler import HyTypeError
from hy.lex import LexException


logger = logging.getLogger(__name__)

DEFAULT_MACROS = ""
PLAYBOOK_GLOBALS = {}


class PlaybookNotFound(RuntimeError):
    pass


def _globals(mod):
    g = mod.__dict__.copy()
    g.update(PLAYBOOK_GLOBALS)
    return g


def _playbook_contents(fpath):
    """
    Gets the contents of the playbooks as a string.

    Also splices in some macros to the header of the file as
    there appears to be no way to inject macros into the
    global namespace.
    """
    # TODO: Fork hylang to add support to
    global DEFAULT_MACROS

    if not DEFAULT_MACROS:
        p = Path(__file__).parent / 'macros.hy'
        with open(p, 'r', encoding='utf-8') as f:
            DEFAULT_MACROS = f.read() + '\n'

    with open(fpath, 'r', encoding='utf-8') as f:
        return DEFAULT_MACROS + f.read()

    return DEFAULT_MACROS


def load_playbook(fpath: Path):
    """Import content from fpath and puts it into a Python module.
    Returns the module."""
    module_name = 'dotops.playbooks.' + fpath.parent.name

    try:
        buf = _playbook_contents(fpath)
        _ast = import_buffer_to_ast(buf, module_name)
        mod = imp.new_module(module_name)

        mod.__file__ = fpath
        eval(ast_compile(_ast, fpath, "exec"), _globals(mod))
    except (HyTypeError, LexException) as e:
        if e.source is None:
            with open(fpath, 'rt') as fp:
                e.source = fp.read()
            e.filename = fpath
        raise
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return mod


def _exec(module):
    pass
    1


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
