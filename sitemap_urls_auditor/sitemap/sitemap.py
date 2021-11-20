"""This module implements Sitemap class."""


import datetime
import json
import pickle
import time
from typing import Iterator, Optional

import requests
from usp.objects.page import SitemapPage
from usp.objects.sitemap import AbstractSitemap
from usp.tree import sitemap_tree_for_homepage

from sitemap_urls_auditor.logger.main_logger import main_logger
from sitemap_urls_auditor.sitemap.types import (
    GroupedResponses,
    Responses,
    StatusCodesCount,
    Urls,
    UrlsCountByCategory,
)
from sitemap_urls_auditor.sitemap.utils import (
    add_text_to_filename,
    count_dict_values,
    group_dict_by_value,
)


class SiteMap:
    """Represent sitemap for homepage url."""

    _https_prefix = 'https://'
    _error_category = 'errors'
    _correct_category = 'correct'
    _today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    _bad_status_code = 400

    def __init__(self, homepage_url: str) -> None:
        self.homepage_url = homepage_url
        self.urls_filename = self._get_urls_filename()
        self.responses_filename = self._get_responses_filename()
        self.pages = None
        self.responses_count = 0

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        description = '<{cls_name}({homepage_url})>'
        return description.format(
            cls_name=cls_name,
            homepage_url=self.homepage_url,
            )

    def get_all_urls(self) -> Urls:
        self._set_all_pages()
        return [page.url for page in self.pages][:5]  # limit is set!

    def get_or_save_urls(self) -> Urls:
        existing_urls = self._get_urls_from_pickle()
        if existing_urls:
            return existing_urls
        urls = self.get_all_urls()
        self._save_urls_to_pickle(urls)
        return urls

    def get_or_save_responses(self) -> Responses:
        filename = self.responses_filename
        existing_responses = self._get_responses_from_pickle(filename)
        if existing_responses:
            self.responses_count = len(existing_responses)
            return existing_responses
        urls = self.get_or_save_urls()
        responses = self._get_responses_from_urls(urls)
        self.responses_count = len(responses)
        self._save_responses_to_pickle(responses)
        return responses

    def get_urls_grouped_by_status_codes(self) -> GroupedResponses:
        responses = self.get_or_save_responses()
        return group_dict_by_value(responses)

    def save_grouped_status_codes(self) -> None:
        """Get and save urls grouped by status codes to json file."""
        filename = self._get_filename_for_status_codes_json()
        status_codes = self.get_urls_grouped_by_status_codes()
        with open(filename, 'w') as output_file:
            json.dump(status_codes, output_file, indent=4)

    def _get_urls_filename(self) -> str:
        url = self.homepage_url.removeprefix(self._https_prefix)
        filename = 'sitemap_{url}_urls.pickle'
        return filename.format(url=url)

    def _fetch_tree(self) -> AbstractSitemap:
        return sitemap_tree_for_homepage(self.homepage_url)

    def _get_all_pages_from_tree(self) -> Iterator[SitemapPage]:
        tree = self._fetch_tree()
        return tree.all_pages()

    def _set_all_pages(self) -> None:
        self.pages = self._get_all_pages_from_tree()

    def _save_urls_to_pickle(self, urls: Urls) -> None:
        with open(self.urls_filename, 'wb') as output_file:
            pickle.dump(urls, output_file)

    def _get_urls_from_pickle(self) -> Optional[Urls]:
        try:
            with open(self.urls_filename, 'rb') as input_file:
                urls = pickle.load(input_file)
        except FileNotFoundError:
            return None
        return urls

    def _get_responses_from_urls(self, urls: Urls) -> Responses:
        responses = {}
        urls_count = len(urls)
        message = '{index} out of {urls_count} -- {status} -- {url}'
        for index, url in enumerate(urls, start=1):
            status = requests.get(url).status_code
            time.sleep(1)
            responses.update({url: status})
            specific_message = message.format(
                index=index,
                urls_count=urls_count,
                status=status,
                url=url,
                )
            if status >= self._bad_status_code:
                main_logger.error(specific_message)
            else:
                main_logger.success(specific_message)
        return responses

    def _get_responses_filename(self) -> str:
        return add_text_to_filename(
            text=['responses', self._today_str],
            filename=self.urls_filename,
            )

    def _save_responses_to_pickle(self, responses: Responses) -> None:
        with open(self.responses_filename, 'wb') as output_file:
            pickle.dump(responses, output_file)

    def _get_responses_from_pickle(self, input_filename: str) -> Responses:
        try:
            with open(input_filename, 'rb') as input_file:
                responses = pickle.load(input_file)
        except FileNotFoundError:
            return None
        return responses

    def _get_urls_count_for_status_codes(
            self, responses: Responses) -> StatusCodesCount:
        return count_dict_values(responses)

    def _sum_urls_by_category(self) -> UrlsCountByCategory:
        responses = self.get_urls_grouped_by_status_codes()
        categorized = {}
        for status, urls in responses.items():
            urls_count = len(urls)
            if status >= self._bad_status_code:
                existing_urls_count = categorized.get(self._error_category, 0)
                new_urls_count = urls_count + existing_urls_count
                categorized.update({self._error_category: new_urls_count})
            else:
                existing_urls_count = categorized.get(self._correct_category, 0)
                new_urls_count = urls_count + existing_urls_count
                categorized.update({self._correct_category: new_urls_count})
        return categorized

    def _get_filename_for_status_codes_json(self) -> str:
        url = self.homepage_url.removeprefix(self._https_prefix)
        filename = 'sitemap_{url}_status_codes_{today_str}.json'
        return filename.format(url=url, today_str=self._today_str)
