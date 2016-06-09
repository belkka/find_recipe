# -*- coding: utf-8 -*-
import re


from database.variables import COLUMNS


def request_mapper(name):
    """
    Конвертирует строку name в шаблон поиска sqlite
    """
    if not isinstance(name, basestring):
        return name

    name = re.sub("\*", "%", name)
    name = re.sub("\?", "_", name)
    name = re.sub("'", "''", name)

    return name


def generate_commands(columns, table):
    selector = "SELECT {columns} FROM [{table}]"
    writer = "INSERT INTO [{table}]"
    deleter = "DELETE FROM [{table}]"

    d = {'columns': ", ".join(columns), 'table': table}

    def insert_names(string):
        return string.format(**d)

    return map(insert_names, (selector, writer, deleter,))


def row_to_dict(row, selector_key):
    return dict(zip(COLUMNS[selector_key], row))


def what_user_want(record):
    """
    Если результат поиска только один и он совпадает с запросом,
    сохранить в record['one'] идентификатор рецепта, иначе сохранить
    None
    """
    record['one'] = None
    if len(record['results']) == 1:
        info = row_to_dict(record['results'][0], 'SEARCH')
        if info["title"] == record['request'].print_:
            record['one'] = str(info["recipe_id"])
