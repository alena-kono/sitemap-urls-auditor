"""Module contains shortcut tools for fetching urls from a sitemap."""

from sitemap_urls_auditor.sitemap.sitemap import SiteMap
from sitemap_urls_auditor.sitemap.types import GroupedResponses
from sitemap_urls_auditor.sitemap.url_collection import GroupedUrlStatusCollection  # noqa: E501


def get_urls_statuses(homepage_url: str) -> GroupedResponses:
    """Fetch urls from a sitemap with `homepage_url`.

    Args:
        homepage_url:
            Url of target site's homepage, for example
            `https://google.com/'`.

    Returns:
        Urls grouped by status codes.

        >>> {
                200: ['https://google.com', 'https://something.net'],
                404: ['https://notfoundweb.com'],
            }
    """
    urls = SiteMap(homepage_url).get_all_urls()
    return GroupedUrlStatusCollection(urls).group_by_status_code()
