"""Module implements Sitemap class."""


from typing import Iterator

from usp.objects.page import SitemapPage
from usp.objects.sitemap import AbstractSitemap
from usp.tree import sitemap_tree_for_homepage

from sitemap_urls_auditor.sitemap.types import Urls


class SiteMap(object):
    """Represent sitemap for homepage url."""

    def __init__(self, homepage_url: str) -> None:
        """Init SiteMap class.

        Args:
            homepage_url: URL of a homepage. Example: 'https://example.com'.
        """
        self.homepage_url = homepage_url
        self.responses_count = 0

    def __repr__(self) -> str:
        """Represent a `SiteMap` object.

        Returns:
            <SiteMap(self.homepage.url)>.
        """
        cls_name = self.__class__.__name__
        description = '<{cls_name}({homepage_url})>'
        return description.format(
            cls_name=cls_name,
            homepage_url=self.homepage_url,
            )

    def get_all_urls(self) -> Urls:
        """Get urls from `Sitemap` object's pages.

        Returns:
            Urls - a list of urls.
        """
        pages = self._get_all_pages_from_tree()
        return [page.url for page in pages]

    def _fetch_tree(self) -> AbstractSitemap:
        return sitemap_tree_for_homepage(self.homepage_url)

    def _get_all_pages_from_tree(self) -> Iterator[SitemapPage]:
        tree = self._fetch_tree()
        return tree.all_pages()
