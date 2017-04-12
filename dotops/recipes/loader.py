import os
import sys
import imp
import logging
from typing import Iterable

from pathlib import Path

from hy.importer import import_file_to_ast, ast_compile
from hy.compiler import HyTypeError
from hy.lex import LexException

from .components import Recipe, Task


logger = logging.getLogger(__name__)

DEFAULT_MACROS = ""


class RecipeNotFound(RuntimeError):
    pass


def _globals(root, module):
    module.__dict__['recipe'] = Recipe.constructor(root)
    module.__dict__['task'] = Task
    return module.__dict__


def find_recipe(root: Path) -> Path:
    filenames = ['recipe', 'recipe.hy']

    for filename in filenames:
        path = root / filename
        if path.exists():
            return path
    raise RuntimeError('No recipe(.hy) found.')


def load_recipe(root: Path) -> None:
    """Import content from fpath and puts it into a Python module.
    Returns the module."""
    module_name = 'dotops.recipes.' + root.name
    fpath = find_recipe(root)

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


def load_recipes(recipes: Iterable[Path]):
    for root in recipes:
        load_recipe(root)


def exec_loaded():
    for recipe_path in Recipe.ALL:
        recipe = Recipe.ALL[recipe_path]
        recipe.execute()
