"""Module contains functions that serve cli package."""


def convert_to_string(sep: str, **kwargs) -> str:
    """Convert `**kwargs` to string and concatenate them using separator.

    Args:
        sep:
            Separator to be used to separate each keyword argument.
        kwargs:
            Keyword arguments to be unpacked and converted
            to string using separator.

    Returns:
        Concatenated string.

    Example:
        >>> convert_to_string(sep=' --> ', status=200, url='google.com')
        >>> 'status=200 --> url=google.com'
    """
    template = '{0}={1}'
    unpacked_kwargs = (
        template.format(key, arg) for key, arg in kwargs.items()
        )
    return sep.join(unpacked_kwargs)
