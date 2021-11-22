"""Module contains helper-functions that serve sitemap package."""


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
