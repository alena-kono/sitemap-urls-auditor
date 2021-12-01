"""Module contains custom types."""

from typing import Dict, List

Url = str
Urls = List[Url]

Responses = Dict[Url, int]
GroupedResponses = Dict[int, Url]
StatusCodesCount = Dict[int, int]
UrlsCountByCategory = Dict[str, int]
