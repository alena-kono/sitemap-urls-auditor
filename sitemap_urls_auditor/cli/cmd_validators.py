"""Module contains validator functions."""


def is_json_filename(filename: str) -> bool:
    """Check whether filename represents a json file.

    Args:
        filename:
            UNIX filename of .json file,
            for example - '/Users/king/urls.json'.

    Returns:
        Boolean, True if json filename is valid,
        otherwise False.

    Example:
        >>> is_json_filename_valid(filename='/Users/king/urls.json')
        >>> True
        >>> is_json_filename_valid(filename='/Users/king/urls.incorrectext')
        >>> False
    """
    valid_extension = '.json'
    extension = filename[-len(valid_extension):]
    return valid_extension == extension
