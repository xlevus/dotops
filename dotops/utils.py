import os
import sys
import logging
from itertools import chain
from pathlib import Path
from typing import Optional, Iterable

logger = logging.getLogger(__name__)


def import_string(import_name):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).
    If `silent` is True the return value will be `None` if the import fails.
    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    # __import__ is not able to handle unicode strings in the fromlist
    # if the module is a package
    import_name = str(import_name).replace(':', '.')

    try:
        __import__(import_name)
    except ImportError:
        if '.' not in import_name:
            raise
    else:
        return sys.modules[import_name]

    module_name, obj_name = import_name.rsplit('.', 1)
    try:
        module = __import__(module_name, None, None, [obj_name])
    except ImportError:
        # support importing modules not yet set up by the parent module
        # (or package for that matter)
        module = import_string(module_name)

    try:
        return getattr(module, obj_name)
    except AttributeError as e:
        raise ImportError(e)


def indent_string(string: str, indent="\t"):
    lines = string.splitlines()
    joiner = "\n" + indent
    return indent + joiner.join(lines)


def path_is_executable(path: Path) -> bool:
    if not path.exists():
        logger.debug("{} does not exist".format(path))
        return False

    if not os.access(path, os.X_OK):
        logger.warn("{} is not +x".format(path))
        return False

    return True


def find_executable(*names: str,
                    additional_roots: Iterable[Path] = (),
                    additional_files: Iterable[Path] = ())-> Optional[Path]:
    """Finds an executable on $PATH matching one of `names`.

    Also searches any files in `additional_roots`, and any `additional_files`.
    """
    for path in additional_files:
        if path_is_executable(path):
            return path

    for root in chain(additional_roots, os.get_exec_path()):
        root = Path(root)
        for name in names:
            path = root / name
            if path_is_executable(path):
                return path
    return None
