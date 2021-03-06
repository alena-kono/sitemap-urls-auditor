"""Module implements classes that manipulate collections of urls."""

import time

import requests

from sitemap_urls_auditor.sitemap.dict_tools import get_value_len, transpose
from sitemap_urls_auditor.sitemap.types import (
    GroupedResponses,
    Responses,
    StatusCodesCount,
    Urls,
    UrlsCountByCategory,
)


class UrlStatusCollection(object):
    """Represent urls and their response status codes.

    Args:
        urls: A list of urls.
    """

    def __init__(self, urls: Urls) -> None:
        """Init UrlStatusCollection class.

        Args:
            urls: A list of urls.
        """
        self.urls = urls
        self.responses: Responses = {}

    def fetch_status_codes(self) -> Responses:
        """Get response statuses for each url in `self.urls`.

        Send GET request to each url in `self.urls`, extract status
        code from each response and save it to `self.responses` dict.

        Returns:
            Responses: A dict with urls as keys and response
            statuses as values.

        Example:
            >>> urls = [
                'https://something.net/news',
                'https://something.net/blogs,
                'https://something.net/not-found',
                ]
            >>> sitemap = UrlStatusCollection(urls=urls)
            >>> sitemap.fetch_status_codes()
            >>> {
                'https://something.net/news': 200,
                'https://something.net/blogs': 200,
                'https://something.net/not-found': 404,
                }
        """
        for url in self.urls:
            status = requests.get(url).status_code
            time.sleep(1)
            self.responses.update({url: status})
        return self.responses


class GroupedUrlStatusCollection(UrlStatusCollection):
    """Represent grouped urls and their response status codes.

    Args:
        urls: A list of urls.
    """

    _error_category = 'error'
    _success_category = 'success'
    _bad_status_code = 400

    def __init__(self, urls: Urls) -> None:
        """Init GroupedUrlStatusCollection class.

        Args:
            urls: A list of urls.
        """
        super().__init__(urls)
        self.responses = self.fetch_status_codes()
        self.urls_by_status_code: GroupedResponses = {}

    def group_by_status_code(self) -> GroupedResponses:
        """Group urls by their response status codes.

        Returns:
            `dict()` object where keys are response status codes
            and values are `list()` objects containing appropriate urls.

        Example:
            >>> urls = {
                'https://google.com': 200,
                'https://something.net': 200,
                'https://notfoundweb.com': 404,
            }
            >>> grouped_urls = GroupedUrlStatusCollection(urls)
            >>> grouped_urls.group_by_status_code()
            >>> {
                    200: ['https://google.com', 'https://something.net'],
                    404: ['https://notfoundweb.com'],
                }
        """
        return transpose(self.responses)

    def get_count_by_status_codes(self) -> StatusCodesCount:
        """Count urls by their status codes.

        Important note: This method is not in use of CLI app yet.

        Returns:
            `dict()` object where keys are response status codes
            and values are  count of appropriate urls.

        Example:
            >>> urls = {
                'https://google.com': 200,
                'https://something.net': 200,
                'https://notfoundweb.com': 404,
            }
            >>> grouped_urls = GroupedUrlStatusCollection(urls)
            >>> grouped_urls.get_count_by_status_codes()
            >>> {
                    200: 2,
                    404: 1,
                }
        """
        self._get_or_set_urls_by_status_code()
        return get_value_len(self.urls_by_status_code)

    def group_by_category(self) -> UrlsCountByCategory:
        """Group urls by one of the two categories - success or error one.

        'success' category is assigned when response status code is more
        or equal to 400.

        'error' category is assigned when response status code is
        less than 400.

        Important note: This method is not in use of CLI app yet.

        Returns:
            `dict()` object where keys are category name
            and values are count of appropriate urls.

        Example:
            >>> urls = {
                'https://google.com': 200,
                'https://something.net': 200,
                'https://notfoundweb.com': 404,
            }
            >>> grouped_urls = GroupedUrlStatusCollection(urls)
            >>> grouped_urls.group_by_category()
            >>> {
                    'success': 2,
                    'error': 1,
                }
        """
        self._get_or_set_urls_by_status_code()
        urls_by_category = {
            self._success_category: 0,
            self._error_category: 0,
        }
        for status, urls in self.urls_by_status_code.items():

            if status < self._bad_status_code:
                category = self._success_category
            else:
                category = self._error_category

            existing_urls_count = urls_by_category.get(category, 0)
            urls_by_category.update(
                {category: existing_urls_count + len(urls)},
            )
        return urls_by_category

    def _get_or_set_urls_by_status_code(self) -> GroupedResponses:
        if self.urls_by_status_code:
            return self.urls_by_status_code
        self.urls_by_status_code = self.group_by_status_code()
        return self.urls_by_status_code
