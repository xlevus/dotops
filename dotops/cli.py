import logging
from typing import Union

from dotops.context import context


def set_log_level(level: Union[None, str] = None) -> None:
    """Sets the log level on the default logger and current context.
    If no level is specified, level is inferred from context.
    """
    if level is None:
        try:
            level = context.logging
        except AttributeError:
            level = 'CRITICAL'
    else:
        context.logging = level

    logging.basicConfig(level=level)
