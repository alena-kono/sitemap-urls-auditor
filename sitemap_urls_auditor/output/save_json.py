"""Module contains functions responsible for writting data to json."""

import json


def save_to_json(data_object: object, filename: str) -> None:
    """Save data to a json file.

    Args:
        data_object:
            Object to be dumped to a json file.
        filename:
            UNIX filename of target .json file,
            for example - '/Users/king/urls.json'.
    """
    with open(filename, 'w') as output_file:
        json.dump(data_object, output_file, indent=4)
