"""Module contains functions that serve writing data to stdout."""

from sitemap_urls_auditor.cli.convert import convert_to_string
from sitemap_urls_auditor.logger.main_logger import main_logger


def write_to_stdout(
    is_success: bool,
    index: int,
    total_count: int,
    **kwargs,
) -> None:
    """Write `**kwargs` to stdout using loguru logger.

    Args:
        is_success:
            If True, loguru will write success log record to stdout,
            otherwise error log record will be written.
        index:
            Index of a record.
        total_count:
            Total count of records.
        kwargs:
            Key-value pairs to be written to stdout.

    Example:
        >>> write_to_stdout(
            is_success=True,
            index=2,
            total_count=10,
            status=200,
            url='google.com'
            )
        Result written to stdout:
        >>> 2021-12-01 20:26:10.921 | SUCCESS  | write_to_stdout:30 -
        2 out of 10 -- status=200 -- url=google.com
    """
    main_msg_template = '{index} out of {total_count} -- '
    main_msg = main_msg_template.format(index=index, total_count=total_count)
    additional_msg = convert_to_string(sep=' -- ', **kwargs)
    final_msg = main_msg + additional_msg
    if is_success:
        main_logger.success(final_msg)
    else:
        main_logger.error(final_msg)
