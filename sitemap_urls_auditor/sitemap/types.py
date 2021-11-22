"""This module contains custom types."""

from typing import Dict, List

Responses = Dict[str, int]
GroupedResponses = Dict[int, str]
StatusCodesCount = Dict[int, int]
Url = str
Urls = List[Url]
UrlsCountByCategory = Dict[str, int]
