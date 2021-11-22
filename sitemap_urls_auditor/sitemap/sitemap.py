"""This module implements Sitemap class."""


from typing import Iterator

from usp.objects.page import SitemapPage
from usp.objects.sitemap import AbstractSitemap
from usp.tree import sitemap_tree_for_homepage

from sitemap_urls_auditor.sitemap.types import Urls


class SiteMap:
    """Represent sitemap for homepage url."""

    def __init__(self, homepage_url: str) -> None:
        self.homepage_url = homepage_url
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

    def _fetch_tree(self) -> AbstractSitemap:
        return sitemap_tree_for_homepage(self.homepage_url)

    def _get_all_pages_from_tree(self) -> Iterator[SitemapPage]:
        tree = self._fetch_tree()
        return tree.all_pages()

    def _set_all_pages(self) -> None:
        self.pages = self._get_all_pages_from_tree()
