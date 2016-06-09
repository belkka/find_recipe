# -*- coding: utf-8 -*-


from database.utils import row_to_dict
from database.worker import CATEGORIES, calculate_rating
from interface.utils import mark, maplines, ul, ol
from interface.variables import MESSAGES
from recover_ingredients import recover


def print_rating(content_id):
    rating, voices = calculate_rating(content_id)
    if rating is None:
        return ""

    rating_indicator = mark("%.1f" % rating, 'rating')
    voices_indicator = mark("%d" % voices, 'voices')

    return " ".join((rating_indicator, voices_indicator))


def print_result(row, favorites=False):
    result = row_to_dict(row, 'SEARCH')
    result['category'] = CATEGORIES[result['category']]
    result['rating'] = print_rating(result['recipe_id'])
    result['category_icon'] = mark(None, 'category', result['category'])

    message_key = 'print_favorite' if favorites else 'print_result'

    return MESSAGES[message_key].format(**result)


_IMG_DELIMITER = u" |IMG| "


def print_recipe(row):
    recipe = row_to_dict(row, 'RECIPE')

    # Добавление переносов, удалить строку при необходимости
    recipe['ingredients'] = maplines(recover, recipe['ingredients'])

    recipe['ingredients'] = maplines(ul(), recipe['ingredients'])
    recipe['directians'] = maplines(ol('number'), recipe['directians'])
    recipe['rating'] = print_rating(recipe['recipe_id'])
    recipe['img'] = "".join((_IMG_DELIMITER, recipe['img'], _IMG_DELIMITER))

    return MESSAGES['print_recipe'].format(**recipe).split(_IMG_DELIMITER)
