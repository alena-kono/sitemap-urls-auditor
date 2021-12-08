"""Module implements CLI interface."""

from typing import Optional

import typer
import validators

from sitemap_urls_auditor.cli.cmd_messages import (
    send_error_msg_invalid_json_filename,
    send_error_msg_invalid_url,
    send_success_msg_saved_to_json,
)
from sitemap_urls_auditor.cli.cmd_validators import is_json_filename
from sitemap_urls_auditor.cli.init_app import app
from sitemap_urls_auditor.output.save_json import save_to_json
from sitemap_urls_auditor.output.stdout import write_to_stdout_pager
from sitemap_urls_auditor.sitemap.shortcuts import get_urls_statuses


@app.command()
def process_main_cmd(url: str, filename: Optional[str] = None) -> None:
    """Get sitemap and fetch response status code for each url.

    Args:
        url:
            Homepage url, for example `https://google.com/'`.
            Used for fetching sitemap.
        filename:
            UNIX filename of .json file where result will be
            saved, for example - '/Users/king/urls.json'. If not given,
            result will be displayed via default pager.

    Returns:
        None, but print result to stdout or a file.
    """
    if not validators.url(url):
        send_error_msg_invalid_url(url=url)
        typer.Exit(code=1)
        return None
    if filename and not is_json_filename(filename):
        send_error_msg_invalid_json_filename(filename)
        typer.Exit(code=1)
        return None

    urls_statuses = get_urls_statuses(url)

    if filename:
        save_to_json(data_object=urls_statuses, filename=filename)
        send_success_msg_saved_to_json(filename)
        return None
    else:
        write_to_stdout_pager(urls_statuses)


if __name__ == '__main__':
    app()
