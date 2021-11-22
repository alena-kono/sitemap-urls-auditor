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
        self._filename = self._get_responses_filename()

    def get_or_save_responses(self) -> Responses:
        existing_responses = self._get_responses_from_pickle(self._filename)
        if existing_responses:
            self.responses = existing_responses
            return self.responses
        responses = self._get_responses()
        self._save_responses_to_pickle()
        return responses

    def _get_responses(self) -> Responses:
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

    def _get_responses_filename(self) -> str:
        homepage_url = self._parse_homepage_url()
        base_filename = '{0}.pickle'.format(homepage_url)
        today = get_today_str()
        return add_text_to_filename(
            text=['responses', today],
            filename=base_filename,
            )

    def _parse_homepage_url(self) -> str:
        first_url = self.urls[0]
        first_url_no_prefix = first_url.removeprefix(self._https_prefix)
        return first_url_no_prefix.split('/')[0]

    def _save_responses_to_pickle(self) -> None:
        with open(self._filename, 'wb') as output_file:
            pickle.dump(self.responses, output_file)

    def _get_responses_from_pickle(
        self,
        filename: str,
    ) -> Union[Responses, NoReturn]:
        try:
            with open(filename, 'rb') as input_file:
                responses = pickle.load(input_file)
        except FileNotFoundError:
            return None
        return responses


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
        self.responses = self.get_or_save_responses()
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

    def _get_filename_for_status_codes_json(self) -> str:
        homepage_url = self._parse_homepage_url()
        today = get_today_str()
        return add_text_to_filename(
            text=[homepage_url, today],
            filename='sitemap_status_codes.json',
            )
