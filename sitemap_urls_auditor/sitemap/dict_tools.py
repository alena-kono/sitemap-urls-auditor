"""Module contains helper-functions that serve sitemap package."""


def get_value_len(dct: dict) -> dict:
    """Get length of each dictionary value.

    Args:
        dct: Python `dict()` object.

    Returns:
        `dict()` object.

    Example:
        >>> status_codes = {
                200: ['google.com', 'something.net'],
                404: ['notfoundweb.com'],
            }
        >>> get_value_len(dct=status_codes)
        >>> {
            200: 2,
            404: 1,
            }
    """
    counter = {}
    for key, nested_container in dct.items():
        counter[key] = len(nested_container)
    return counter


def transpose_dict(dct: dict):
    """Transpose `dct`.

    Args:
        dct: Python `dict()` object.

    Returns:
        `dict()` object.

    Example:
        >>> urls = {
            'google.com': 200,
            'something.net': 200,
            'notfoundweb.com': 404,
        }
        >>> transpose_dict(dct=urls)
        >>> {
            200: ['google.com', 'something.net'],
            404: ['notfoundweb.com'],
            }
    """
    grouped = {}
    for key, transposable in dct.items():
        grouped.setdefault(transposable, []).append(key)
    return grouped
