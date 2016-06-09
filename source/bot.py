# -*- coding: utf-8 -*-

# Author: Ulyanich Michael
# Telegram: @belkka
# Mail: ulianich_mihail@ukr.net
#
# sorry for my English

import re
import urllib       # |
# import urllib2    # |  Temporary
# import requests   # |

import telebot as tb

import config
import database as db
from interface import navigation as nav
from interface import output
from interface.variables import MESSAGES
import log


# Last search results for each user
user_results = {}

photo_id = {}


class Request:
    def __init__(self, text=None, search_type=None, words=None):
        if search_type is None:
            text = re.sub(" +", " ", text)

            if ":" in text:
                search_type, text = text.split(":", 1)
                if search_type not in {"TIT", "ING", "CAT", "FAV"}:
                    text = ":".join((search_type, text))
                    search_type = None

            self.words = tuple(w.strip()
                               for w in text.split(",")
                               if not w.isspace())

            if search_type is None:
                self.search_type = "TIT" if len(self.words) == 1 else "ING"
            else:
                self.search_type = search_type
        else:
            self.words = words
            self.search_type = search_type

        if self.search_type == "FAV":
            self.print_ = "Favorites"
        else:
            self.print_ = text

    def search(self):
        if self.search_type == "TIT":
            connection = db.worker.by_title
        elif self.search_type == "ING":
            connection = db.worker.by_ingredients
        elif self.search_type == "CAT":
            connection = db.worker.by_category
        elif self.search_type == "FAV":
            connection = db.worker.by_id

        return connection.select(*self.words)

    def to_str(self):
        text = ", ".join(str(word) for word in self.words)
        return ": ".join((self.search_type, text)) if text != "" else ""


def update_results(chat_id, request):
    global user_results

    if chat_id in user_results:
        if request == user_results[chat_id]['request']:
            return   # caching

    user_results[chat_id] = {
        'request': request,
        'results': request.search(),
    }

    db.utils.what_user_want(user_results[chat_id])


def get_page(chat_id, current_page):
    global user_results

    if chat_id not in user_results:
        return MESSAGES['no_user_id'](chat_id), None

    rpp = config.RES_PER_PAGE

    request = user_results[chat_id]['request']
    results = user_results[chat_id]['results']
    last_page = (len(results) + rpp - 1) // rpp

    last_result = len(results)

    if not results:
        return MESSAGES['no_results'](request.print_), None
    else:
        favorites = (request.search_type == "FAV")
        if favorites:
            answer = MESSAGES['favorites'](last_result)
        else:
            answer = MESSAGES['results'](request.print_, last_result)

        if not 1 <= current_page <= last_page:
            raise IndexError("Page is out of range 1..%d" % last_page)

        first_res_on_page = (current_page - 1) * rpp
        last_res_on_page = first_res_on_page + rpp
        last_res_on_page = min(last_res_on_page, last_result)

        page = results[first_res_on_page: last_res_on_page]

        answer += "\n".join((output.print_result(res, favorites)
                             for res in page))

        markup = nav.EmptyKeyboard()
        nav.add_navigation(markup, last_page, current_page, request.to_str())

        return answer, markup


############################################################
# ###################### bot ############################# #
############################################################

bot = tb.TeleBot(config.TOKEN)


def show_image(chat_id, img_url):
    if img_url not in photo_id:
        tmp_img = "tmp.jpg"
        urllib.urlretrieve(img_url, tmp_img)

        with open(tmp_img, "rb") as img:
            res = bot.send_photo(chat_id, img)
            file_id = res.photo[0].file_id

            photo_id[img_url] = file_id
    else:
        img = photo_id[img_url]
        bot.send_photo(chat_id, img, disable_notification=True)


def show_recipe(chat_id, recipe_id):
    payload = {
        'chat_id': chat_id,
        'parse_mode': "HTML",
        'disable_notification': True
    }

    result = db.worker.recipe.select(recipe_id)

    if not result:
        log.bot.warning("No recipe id %s. User id: %d", recipe_id, chat_id)
        bot.send_message(text=MESSAGES['no_recipe_id'](recipe_id), **payload)
    else:
        part1, img_url, part2 = output.print_recipe(result[0])

        markup = nav.recipe_grid(recipe_id, chat_id)

        bot.send_message(text=part1, **payload)
        show_image(chat_id, img_url)
        bot.send_message(text=part2, reply_markup=markup, **payload)


def show_page(chat_id, current_page=1, message_id=None):
    try:
        answer, keyboard = get_page(chat_id, current_page)
    except IndexError as e:
        log.bot.exception("Can't get page %d", current_page)
        return

    payload = {
        'chat_id': chat_id,
        'text': answer,
        'reply_markup': keyboard,
        'parse_mode': "HTML"
    }

    if message_id is None:
        bot.send_message(**payload)
    else:
        bot.edit_message_text(message_id=message_id, **payload)


############################
#        Handlers          #
############################


def quick_answer(answer):
    def quick_handler(message):
        text, markup = answer(message.chat.id, message.text)
        payload = {
            'chat_id': message.chat.id,
            'text': text,
            'reply_markup': markup,
            'parse_mode': "HTML",
        }
        bot.send_message(**payload)
    return quick_handler


@bot.message_handler(regexp=config.REGEXP_START)
@quick_answer
def show_start_message(chat_id, text):
    return MESSAGES['/start'], None


@bot.message_handler(regexp=config.REGEXP_AF)
@quick_answer
def add_favorite(chat_id, text):
    recipe_id = re.match(config.REGEXP_AF, text).group(1)
    db.worker.favorites.insert(chat_id, recipe_id)
    return "Done.", None


@bot.message_handler(regexp=config.REGEXP_RF)
@quick_answer
def remove_favorite(chat_id, text):
    recipe_id = re.match(config.REGEXP_RF, text).group(1)
    db.worker.favorites.delete(chat_id, recipe_id)
    return "Done.", None


@bot.message_handler(regexp=config.REGEXP_CATEGORIES)
@quick_answer
def show_categories(chat_id, text):
    return MESSAGES['categories_list'], nav.categories_menu(),


@bot.message_handler(regexp=config.REGEXP_FAVORITE)
@quick_answer
def show_favorites(chat_id, text):
    favorites = sum(db.worker.favorites.select(chat_id), tuple())
    request = Request(search_type="FAV", words=favorites)
    update_results(chat_id, request)
    return get_page(chat_id, 1)


@bot.message_handler(regexp=config.REGEXP_OPEN)
def open_recipe(message):
    chat_id = message.chat.id
    request = message.text

    recipe_id = re.search(config.REGEXP_OPEN, request).group(1)

    show_recipe(chat_id, recipe_id)


@bot.message_handler(content_types=['text'])
def open_search_results(message):
    chat_id = message.chat.id

    update_results(chat_id, Request(message.text))

    one = user_results[chat_id]['one']
    if one is not None:
        show_recipe(chat_id, one)
    else:
        show_page(chat_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    log.bot.debug(call.data)
    try:
        t, data = call.data.split(':', 1)
    except ValueError as e:
        log.bot.exception("Incorrect callback data: %s", repr(call.data))
        return

    payload = {
        'chat_id': call.from_user.id,
        'message_id': call.message.message_id
    }
    chat_id = str(call.from_user.id)

    if t.isdigit():  # change page
        page = int(t, 10)
        update_results(payload['chat_id'], Request(data))
        show_page(current_page=page, **payload)

    else:
        if t == 'VG':  # open Vote Grid
            payload['reply_markup'] = nav.vote_grid(data)

        elif t == 'V':  # Vote
            vote, recipe_id = data.split(' ', 1)
            db.worker.voices_list.insert(chat_id, recipe_id, vote)
            payload['reply_markup'] = nav.recipe_grid(recipe_id, chat_id)

        elif t == 'AF':  # Add to Favorites
            recipe_id = data
            db.worker.favorites.insert(chat_id, data)
            payload['reply_markup'] = nav.recipe_grid(recipe_id, True)

        elif t == 'RF':  # Remove from Favorites
            recipe_id = data
            db.worker.favorites.delete(chat_id, recipe_id)
            payload['reply_markup'] = nav.recipe_grid(recipe_id, False)

        else:
            log.bot.warning("Incorrect callback type: %s", t)
            return

        bot.edit_message_reply_markup(**payload)


if __name__ == "__main__":
    bot.polling(none_stop=True)
