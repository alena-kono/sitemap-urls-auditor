"""Module contains helper-functions that serve sitemap package."""

import datetime
from typing import List


def get_nested_len(d: dict) -> dict:
    counter = {}
    for key, value in d.items():
        counter[key] = len(value)
    return counter


def group_dict_by_value(d: dict):
    grouped = {}
    for key, val in d.items():
        grouped.setdefault(val, []).append(key)
    return grouped


def add_text_to_filename(text: List[str], filename: str) -> str:
    extension_sep = '.'
    parts = list(filename.partition(extension_sep))
    name_part = parts[:1]
    extension_part = ''.join(part for part in parts[-2:])
    name_part.extend(text)
    new_name = '_'.join(part for part in name_part)
    return new_name + extension_part


def get_today_str(fmt: str = '%Y-%m-%d') -> str:
    return datetime.datetime.today().strftime(fmt)
