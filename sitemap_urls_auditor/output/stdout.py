"""Module implement functions responsible for writting data to stdout."""


import json

import typer


def write_to_stdout_pager(data_object: object) -> None:
    """Write to stdout default pager.

    Args:
        data_object:
            Object to be converted to json string
            and then written to stdout default pager.
    """
    json_str = json.dumps(data_object, indent=4)
    typer.echo_via_pager(json_str)


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
