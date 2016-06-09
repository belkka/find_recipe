# -*- coding: utf-8 -*-


class CON:
    ID = "recipe_id"
    TITLE = "title"
    CATEGORY = "category"
    INGREDIENTS = "ingredients"
    DIRECTIANS = "directians"
    TIME = "time"
    IMAGE = "img"


class CAT:
    ID = "id"
    TITLE = "title"


class RAT:
    USER = "user_id"
    CONTENT = "content_id"
    VOICE = "voice"
    SUM = "SUM(voice)"
    COUNT = "COUNT(*)"
    AVG = "AVG(voice)"


class FAV:
    USER = "user_id"
    CONTENT = "content_id"


"""
Типы обращений к базе данных = {
    'SEARCH': обращение для отображения результатов поиска.
               Необходимо извлечь из таблицы [content] данные о
               идентификаторе, заголове и категории блюда

    'RECIPE': обращение для отображения рецепта.
               Необходимо извлечь из таблицы [content] данные
               о идентификаторе, заголовке, игридиентах, адресе
               изображения и рецепте блюда

    'CATEGORIES': обращение для установления соответствия между
                   идентификатором и названием категории.
                   Их нужно извлечь из таблицы [category]

    'RATING': обращение для вычисления рейтинга рецепта. Необходимо
              извлечь из таблицы [rating] сумму и количество голосов.

    'VOICE': обращение для сохранения данных о голосе в таблицу [rating]

    'FAVORITES': обращение для определения избранных рецептов. Необходимо
                 извлечь из таблицы [favorites] идентификаторы рецептов.
"""

COLUMNS = {
    'SEARCH': (CON.ID, CON.TITLE, CON.CATEGORY),
    'RECIPE': (CON.ID, CON.TITLE, CON.INGREDIENTS,
               CON.IMAGE, CON.DIRECTIANS),
    'CATEGORIES': (CAT.ID, CAT.TITLE),
    'RATING': (RAT.SUM, RAT.COUNT),
    'VOICE': (RAT.USER, RAT.CONTENT, RAT.VOICE),
    'FAVORITES': (FAV.CONTENT,),
}

TABLE_NAME = {
    'SEARCH': "content",
    'RECIPE': "content",
    'CATEGORIES': "category",
    'RATING': "rating",
    'VOICE': "rating",
    'FAVORITES': "favorites",
}
