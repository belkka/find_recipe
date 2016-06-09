# -*- coding: utf-8 -*-


from interface.variables import ICONS


def mark(string, icon_key, key=None):
    iconset = ICONS[icon_key]

    if isinstance(iconset, dict) and key not in iconset:
        key = None

    icon = iconset[key] if isinstance(iconset, (tuple, dict)) else iconset

    return icon if string is None else " ".join((icon, string))


def rating_stars(rating):
    return ICONS['star'] * rating


def maplines(mapper, data):
    return "\n".join(mapper(data.splitlines()))  # split, map, reduce!


def ul(icon_key='ingredient'):
    """
    Unordered list
    Возвращает mapper. mapper добавляет иконку ICONS[icon_key] из
    модуля interface.variables к каждой строке списка lines.
    """
    def mapper(lines):
        for line in lines:
            yield mark(line, icon_key)
    return mapper


def ol(icon_sequence_key='number'):
    """
    Ordered list
    Возвращает mapper. mapper последовательно добавляет иконки из
    списка ICONS[icon_sequence_key] модуля interface.variables к каждой
    строке списка lines.
    """
    def mapper(lines):
        for (i, line) in enumerate(lines):
            yield mark(line, icon_sequence_key, i)
    return mapper
