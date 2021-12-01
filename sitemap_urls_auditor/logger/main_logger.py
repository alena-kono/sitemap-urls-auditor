"""Module configures project's main logger."""

import logging
from typing import Union

from loguru import logger


def disable_usp_logging(level: Union[str, int]) -> None:
    """Disable logging of ultimate-sitemap-parser (usp) library.

    Args:
        level: Logging level to be set for usp library loggers.
    """
    logging.getLogger('usp.helpers').setLevel(level)
    logging.getLogger('usp.fetch_parse').setLevel(level)
    logging.getLogger('usp.tree').setLevel(level)


def get_loguru_logger():
    """Get loguru Logger object.

    Returns:
        Loguru Logger object.
    """
    return logger


disable_usp_logging(level=logging.ERROR)
main_logger = get_loguru_logger()
