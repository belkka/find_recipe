# -*- coding: utf-8 -*-

import telebot.types as tb_types

from database.worker import CATEGORIES, favorites
from interface.variables import BUTTON_DECORATOR, BUTTON_TEXT
from interface.utils import mark, rating_stars


def Button(text, cb_type, *args):
    cbd = ':'.join((cb_type, ' '.join(args)))
    return tb_types.InlineKeyboardButton(text, callback_data=cbd)


def EmptyKeyboard():
    return tb_types.InlineKeyboardMarkup()


def button_maker(last_page, current_page, center, data):
    def make_inline_keyboard_button(num):
        status = 'normal'

        if center != -2:
            if current_page > 1 + 2:
                if num == 1:
                    status = 'first'

                elif num == center - 1:
                    status = 'previous'

            if current_page < last_page - 2:
                if num == last_page:
                    status = 'last'

                elif num == center + 1:
                    status = 'next'

        if num == current_page:
            status = 'current'

        text = BUTTON_DECORATOR[status](num)

        return Button(text, str(num), data)

    return make_inline_keyboard_button


def add_navigation(markup, last_page, current_page, data):
    if last_page <= 1:
        return

    if last_page < 5:
        center = -2
        nav = range(1, last_page + 1)
    else:
        center = current_page
        center = max(center, 1 + 2)
        center = min(center, last_page - 2)
        nav = [1] + range(center - 1, center + 2) + [last_page]

    buttons = map(button_maker(last_page, current_page, center, data), nav)
    markup.row(*buttons)


def categories_menu():
    markup = EmptyKeyboard()
    for (data, name) in CATEGORIES.iteritems():
        markup.row(Button(mark(name, 'category', name), '1',
                          "CAT: %d" % data))
    return markup


def vote_grid(recipe_id):
    markup = EmptyKeyboard()
    buttons = tuple(Button(rating_stars(i), 'V', str(i), recipe_id)  # Vote
                    for i in xrange(1, 6))
    markup.row(*buttons[:3])
    markup.row(*buttons[3:])
    return markup


# TODO(@belkka) use user_voice
# is_favorite  - bool or user_id
def recipe_grid(recipe_id, is_favorite, user_voice=None):
    markup = EmptyKeyboard()

    vote_button = Button(BUTTON_TEXT['vote'], 'VG', recipe_id)  # Vote Grid

    if not isinstance(is_favorite, bool):
        user_id = is_favorite
        is_favorite = bool(favorites.select(user_id, recipe_id))

    fb_text = BUTTON_TEXT['favorite'][is_favorite]
    fb_cbd = 'RF' if is_favorite else 'AF'
    favorite_button = Button(fb_text, fb_cbd, recipe_id)

    markup.row(vote_button, favorite_button)
    return markup
