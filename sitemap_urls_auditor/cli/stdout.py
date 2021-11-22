"""This module contains functions that serve writing data to stdout."""

from sitemap_urls_auditor.cli.convert import convert_to_string
from sitemap_urls_auditor.logger.main_logger import main_logger


def write_to_stdout(
    is_success: bool,
    index: int,
    total_count: int,
    **kwargs,
) -> None:
    main_msg_template = '{index} out of {total_count} -- '
    main_msg = main_msg_template.format(index=index, total_count=total_count)
    additional_msg = convert_to_string(sep=' -- ', **kwargs)
    final_msg = main_msg + additional_msg
    if is_success:
        main_logger.success(final_msg)
    else:
        main_logger.error(final_msg)
