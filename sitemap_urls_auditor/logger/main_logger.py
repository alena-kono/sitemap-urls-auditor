"""Module configures project's main logger."""

import logging

from loguru import logger


def disable_usp_logging() -> None:
    """Disable logging of ultimate-sitemap-parser (usp) library.

    Usp package initializes default logging.Logger() each time it
    imports something from its core submodules.

    Therefore, this function disables usp loggers after it imports
    one of the usp functions.
    """
    from usp.tree import sitemap_tree_for_homepage  # noqa: F401, WPS433

    for name, each_logger in logging.root.manager.loggerDict.items():
        if name.startswith('usp') and isinstance(each_logger, logging.Logger):
            each_logger.disabled = True


def get_loguru_logger():
    """Get loguru Logger object.

    Returns:
        Loguru Logger object.
    """
    return logger


main_logger = get_loguru_logger()
