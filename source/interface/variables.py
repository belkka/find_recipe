# -*- coding: utf-8 -*-


from config import (OPEN_COMMAND_KEYWORD,
                    RF_COMMAND_KEYWORD,
                    AF_COMMAND_KEYWORD)

BUTTON_DECORATOR = {
    'first': (lambda n:    u"\u00ab %d" % n),
    'previous': (lambda n: u"\u2039 %d" % n),
    'current': (lambda n:  u"\u00b7 %d \u00b7" % n),
    'next': (lambda n:            u"%d \u203a" % n),
    'last': (lambda n:            u"%d \u00bb" % n),
    'normal': (lambda n:          u"%d" % n)
}


ICONS = {
    'search': u'\U0001f50e',  # 🔎
    'ingredient': u'\U0001f538',  # 🔸
    'rating': u'\u2b50',
    'voices': u'\U0001f465',
    'number': (u"1⃣", u"2⃣", u"3⃣", u"4⃣", u"5⃣",
               u"6⃣", u"7⃣", u"8⃣", u"9⃣", u"🔟"),
    # digit + u'\u20e3'
    'category': {
        'Appetizer': u'🌯',
        'Dessert': u'\U0001f367',
        'Healthy': u'🍵',
        'Quick Show Cooker': u'🍳',
        'Chicken': u'🍗',
        'Holidays': u'🍮',
        'Main Dish': u'🍲',
        'Vegetarian': u'🍵',
        None: u'\U0001f538',  # если категории нет в этом словаре
    },

    'star': u'\u2b50',
    'like': u'\u2764',
    'dislike': u'\U0001f499',
}


MESSAGES = {
    '/start':
        u"Hi, What are we going to cook?",

    'results': (
        lambda request, results_number:
        u"%s <i>Search: %s</i><code>  [%d]</code>"
        u"\n\n" % (ICONS['search'], request, results_number)),

    'favorites': (
        lambda results_number:
        u"%s <i>My favorites</i><code>  [%d]</code>"
        u"\n\n" % (ICONS['like'], results_number)),

    'no_results': (
        lambda request:
        u"Результатов по запросу '%s' нет." % request),

    'no_user_id': (
        lambda user_id:
        u"Ошибка! В базе нет резутьтатов поиска для пользователя с id %d.\n"
        u"Возможно, бот был перезапущен после вашего последнего поиска. "
        u"Попытайтесь повторить поиск." % user_id),

    'no_recipe_id': (
        lambda recipe_id:
        u"Ошибка! В базе нет рецепта с идентификатором %s." % recipe_id),

    'categories_list':
        u"<b>Список категорий</b>",

    'print_result': (
        u"{category_icon} <b>{title}</b>  {rating}\n"
        u"       Category: <i>{category}</i>\n"
        u"       <code>Recipe:</code> /%s{recipe_id}"
        u"  /%s{recipe_id}" % (OPEN_COMMAND_KEYWORD, AF_COMMAND_KEYWORD)),

    'print_recipe': (
        u"{title:^50} {rating}\n"
        u"<b>Ingredients</b>\n"
        u"<i>{ingredients}</i>\n"
        u"{img}\n"
        u"<b>Directians:</b>\n"
        u"{directians}"),

    'print_favorite': (
        u"{category_icon} <b>{title}</b>  {rating}\n"
        u"       Category: <i>{category}</i>\n"
        u"       <code>Recipe:</code> /%s{recipe_id} "
        u"  /%s{recipe_id}" % (OPEN_COMMAND_KEYWORD, RF_COMMAND_KEYWORD)),
}

BUTTON_TEXT = {
    'vote': u"\u2b50 Vote",
    'favorite': (u"{icon} Add to favorites".format(icon=ICONS['like']),
                 u"{icon} Remove from favorites".format(icon=ICONS['dislike']))
}
