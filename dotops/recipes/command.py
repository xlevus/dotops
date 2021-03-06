#!/usr/bin/env python3

import logging
import argparse
from pathlib import Path

from dotops.cli import set_log_level
from dotops.recipes.loader import load_recipes, exec_loaded
from dotops.context import context
from dotops.error_handler import error_handler

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--no-capture', dest='capture_subprocess',
                    default=True, action='store_false')
parser.add_argument('recipes', nargs='+', type=Path)


def apply():
    set_log_level()

    args = parser.parse_args()

    context.capture_output = args.capture_subprocess

    with error_handler:
        load_recipes(args.recipes)
        exec_loaded()
