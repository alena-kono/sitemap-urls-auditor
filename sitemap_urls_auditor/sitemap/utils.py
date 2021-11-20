from typing import List


def count_dict_values(d: dict):
    counter = {}
    for val in d.values():
        existing_val = counter.get(val)
        if existing_val:
            existing_val += 1
            counter.update({val: existing_val})
        else:
            counter.update({val: 1})
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
