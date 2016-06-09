# -*- coding: utf-8 -*-
import sqlite3


from config import DATABASE_PATH
from database.utils import request_mapper, generate_commands
from database.variables import CON, RAT, FAV, COLUMNS, TABLE_NAME
import log


###########################
#         Search          #
###########################

def execute(command, rw):
    assert rw in {'r', 'w'}

    log.sqlite.info(command)

    DB = sqlite3.connect(DATABASE_PATH)
    if rw == 'w':  # write
        DB.execute(command)
        DB.commit()
    else:  # read
        return DB.execute(command)


class CONNECTION:
    """
    Объект для работы с базой данных, возвращает результат
    выполнения команды SELECT <...> FROM <...>
    """

    def __init__(self, key, search_by=None, strong=True):
        """
        key --- ключ словаря SELECTOR из модуля database/variables,
                определяет какие столбцы и из какой таблицы
                выбирать. (str)

        search_by --- если str, то к sqlite запросу добавляется условие
                      WITH <condition>, где search_by --- столбец,
                      значение которого сверяется с шаблонами.
                      если tuple of str, то это столбцы, значения в
                      которых сверяются с соответствующими шаблонами.
                      (str or tuple of str)

        strong --- если True, то соответствие шаблону определяется по
                   оператору "=", иначе по оператору "LIKE". (bool)
        """

        self.selector, self.inserter, self.deleter = generate_commands(
            COLUMNS[key], TABLE_NAME[key]
        )

        if isinstance(search_by, basestring):
            if strong:
                self.matcher = lambda *args: "{0} in ({1})".format(
                    search_by, ", ".join(map("'{}'".format, args)))
            else:
                match = " ".join((search_by, "LIKE '%{}%'"))
                self.matcher = lambda *args: " AND ".join(
                    (match.format(request_mapper(word)) for word in args))

        else:
            if isinstance(search_by, tuple):
                def dic(*args, **kwargs):
                    return zip(search_by, args)
            elif search_by is None:
                def dic(*args, **kwargs):
                    return kwargs.iteritems()

            match_operator = u"{} = {}" if strong else u"{} LIKE '%{}%'"

            def single_matcher(pair):
                return match_operator.format(*pair)

            self.matcher = lambda *args, **kwargs: " AND ".join(
                map(single_matcher, dic(*args, **kwargs)))

    def select(self, *args, **kwargs):
        condition = self.matcher(*args)
        if condition == "":
            command = self.selector
        else:
            command = " ".join((self.selector, "WHERE", condition))
        return execute(command, 'r').fetchall()

    def insert(self, *args):
        data = "VALUES(%s)" % ", ".join(map(str, args))
        command = " ".join((self.inserter, data))
        execute(command, 'w')

    def delete(self, *args, **kwargs):
        condition = self.matcher(*args, **kwargs)
        command = " ".join((self.deleter, "WHERE", condition))
        execute(command, 'w')


by_title = CONNECTION('SEARCH', CON.TITLE, False)
by_ingredients = CONNECTION('SEARCH', CON.INGREDIENTS, False)
by_category = CONNECTION('SEARCH', CON.CATEGORY, True)
by_id = CONNECTION('SEARCH', CON.ID, True)
recipe = CONNECTION('RECIPE', CON.ID, True)

sum_count_voices = CONNECTION('RATING', RAT.CONTENT, True)

voices_list = CONNECTION('VOICE')
favorites = CONNECTION('FAVORITES', (FAV.USER, FAV.CONTENT), True)

# =======================

CATEGORIES = dict(CONNECTION('CATEGORIES').select())


def calculate_rating(content_id):
    """
    Вычисление среднего арифметического рейтингов, выставленных блюду
    с идентификатором content_id (int)
    """
    S, n = sum_count_voices.select(content_id)[0]

    rating = round(float(S) / n, 1) if n != 0 else None

    return rating, n
