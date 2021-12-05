"""Module implement functions responsible for writtening data to stdout."""


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
