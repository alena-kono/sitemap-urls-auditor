"""Module contains notification messages to be sent to stdout."""

import typer

from sitemap_urls_auditor.output.stdout import colorize


def send_error_msg_invalid_json_filename(filename: str) -> None:
    """Send error notification message when invalid json filename is passed.

    Args:
        filename:
            Invalid filename value to be displayed at the error message.
    """
    template = 'Invalid filename for .json file is passed: {0}'
    colored_text = colorize(
        text=template.format(filename),
        success=False,
    )
    typer.echo(colored_text, err=True, color=True)


def send_success_msg_saved_to_json(filename: str) -> None:
    """Send success notification message when json file is saved.

    Args:
        filename:
            Invalid filename value to be displayed at the error message.
    """
    template = 'Urls and status codes are saved to: {0}.'
    colored_text = colorize(
        text=template.format(filename),
        success=True,
    )
    typer.echo(colored_text, err=False, color=True)


def send_error_msg_invalid_url(url: str) -> None:
    """Send error notification message when invalid url is saved.

    Args:
        url:
            Invalid url value to be displayed at the error message.
    """
    template = 'Invalid url is passed: {0}'
    colored_text = colorize(
        text=template.format(url),
        success=False,
    )
    typer.echo(colored_text, err=True, color=True)
