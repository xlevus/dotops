import argparse
import json

from dotops.modules.exec import Module
from dotops.cli import set_log_level

parser = argparse.ArgumentParser()

parser.add_argument('module', nargs='?')
parser.add_argument('data', nargs='?', default='{}')


def main():
    set_log_level()

    args = parser.parse_args()
    module = Module(args.module)

    data = json.loads(args.data)

    module.exec_pretty(data)
