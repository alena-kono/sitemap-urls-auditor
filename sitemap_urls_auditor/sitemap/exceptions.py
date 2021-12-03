"""Module implements exceptions specific for sitemap and urls."""

from sitemap_urls_auditor.base_exceptions import BaseProjectException


class InvalidUrlError(BaseProjectException):
    """To be raised if url is not a valid url."""

    error_template = 'Invalid url is passed: {0}'
