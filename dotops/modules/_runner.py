import os
import sys
import json
import logging

from dotops.utils import import_string
from dotops.cli import set_log_level

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    from ..error_handler import error_handler
    set_log_level()

    with error_handler:
        module = sys.argv[1]
        data = json.loads(sys.argv[2])

        klass = import_string(module)
        inst = klass()

        logger.debug("Executing '{}' in '{}'".format(
            module, os.getcwd()))

        inst.main(**data)
