"""Init typer CLI app."""

import typer

from sitemap_urls_auditor.logger.main_logger import disable_usp_logging


def init_typer_app() -> typer.Typer:
    """Init typer CLI app.

    Also disable ultimate-sitemap-parser (usp) library's loggers.

    Returns:
        typer.Typer() object.
    """
    disable_usp_logging()
    return typer.Typer()


app = init_typer_app()
