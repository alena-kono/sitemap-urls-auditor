"""Module contains functions that serve writing data to stdout."""

import typer


def colorize(text: str, success: bool = True) -> str:
    """Colorize text to be written to stdout.

    Args:
        text:
            Text to be colorized.
        success:
            If True, text color to be set to green,
            otherwise - to red.

    Returns:
        Text which has green or red color.
    """
    color = 'green' if success else 'red'
    return typer.style(text=text, fg=color)
