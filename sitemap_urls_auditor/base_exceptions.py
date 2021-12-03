"""Module implements base exception for this project."""

from typing import ClassVar


class BaseProjectException(Exception):
    """Generic exception for this project.

    All custom exceptions should be inherited from this one.
    """

    error_template: ClassVar[str]

    def __init__(self, error_value: str) -> None:
        """Init BaseProjectException object.

        Init `self.message` as the result of concatenating
        `self.error_template` and error_value.

        Args:
            error_value: Value that caused an error.
        """
        self.message = self.error_template.format(error_value)
