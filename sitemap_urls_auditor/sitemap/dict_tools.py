"""Module contains helper-functions that serve sitemap package."""


def get_nested_len(dct: dict) -> dict:
    counter = {}
    for key, nested_container in dct.items():
        counter[key] = len(nested_container)
    return counter


def transpose_dict(dct: dict):
    grouped = {}
    for key, transposable in dct.items():
        grouped.setdefault(transposable, []).append(key)
    return grouped
