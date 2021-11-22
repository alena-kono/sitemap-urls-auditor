"""Module configures project's main logger."""

import logging

from loguru import logger


def disable_usp_logging(level: str) -> None:
    logging.getLogger('usp.helpers').setLevel(level)
    logging.getLogger('usp.fetch_parse').setLevel(level)
    logging.getLogger('usp.tree').setLevel(level)


def get_loguru_logger():
    return logger


disable_usp_logging(level=logging.ERROR)
main_logger = get_loguru_logger()
