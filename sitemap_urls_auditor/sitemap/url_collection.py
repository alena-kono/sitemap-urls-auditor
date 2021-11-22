"""Module implements classes that manipulate collections of urls."""

import pickle
import time
from typing import NoReturn, Union

import requests

from sitemap_urls_auditor.cli.stdout import write_to_stdout
from sitemap_urls_auditor.sitemap.types import (
    GroupedResponses,
    Responses,
    StatusCodesCount,
    Urls,
    UrlsCountByCategory,
)
from sitemap_urls_auditor.sitemap.utils import (
    add_text_to_filename,
    get_nested_len,
    get_today_str,
    group_dict_by_value,
)


class UrlStatusCollection:
    """Represent urls and their response status codes.

    Args:
        urls: A list of urls.
    """

    _https_prefix = 'https://'
    _bad_status_code = 400

    def __init__(self, urls: Urls) -> None:
        """Init UrlStatusCollection class.

        Args:
            urls: A list of urls.
        """
        self.urls = urls
        self.responses = {}

    def get_responses(self) -> Responses:
        urls_count = len(self.urls)
        for index, url in enumerate(self.urls, start=1):
            status = requests.get(url).status_code
            time.sleep(1)
            self.responses.update({url: status})

            is_ok_status = status < self._bad_status_code
            write_to_stdout(
                is_success=is_ok_status,
                index=index,
                total_count=urls_count,
                status=status,
                url=url,
                )
        return self.responses


class GroupedUrlStatusCollection(UrlStatusCollection):
    """Represent grouped urls and their response status codes.

    Args:
        urls: A list of urls.
    """

    _error_category = 'error'
    _success_category = 'success'

    def __init__(self, urls: Urls) -> None:
        """Represent InitGroupedUrlStatusCollection class.

        Args:
            urls: A list of urls.
        """
        super().__init__(urls)
        self.responses = self.get_responses()
        self.urls_by_status_code = {}

    def group_by_status_code(self) -> GroupedResponses:
        return group_dict_by_value(self.responses)

    def get_urls_count_for_status_codes(self) -> StatusCodesCount:
        self._get_or_set_urls_by_status_code()
        return get_nested_len(self.urls_by_status_code)

    def group_by_category(self) -> UrlsCountByCategory:
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
