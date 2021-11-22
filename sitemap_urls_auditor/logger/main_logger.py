"""This module configures project's main logger."""

import logging

from loguru import Logger, logger


def disable_usp_logging(level: str) -> None:
    logging.getLogger('usp.helpers').setLevel(level)
    logging.getLogger('usp.fetch_parse').setLevel(level)
    logging.getLogger('usp.tree').setLevel(level)


def get_loguru_logger() -> Logger:
    return logger


disable_usp_logging()
main_logger = get_loguru_logger()
