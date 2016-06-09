# -*- coding: utf-8 -*-

with open("../token.ini") as token_file:
    TOKEN = token_file.readline().rstrip()

DATABASE_PATH = "db.sqlite"
RES_PER_PAGE = 3

OPEN_COMMAND_KEYWORD = u"open_"
AF_COMMAND_KEYWORD = u"add_"
RF_COMMAND_KEYWORD = u"del_"

REGEXP_START = ur"(?i)^ *((/start)|([Пп]ривет)|(salut)|(hi)|(hello))( .*)?$"
REGEXP_OPEN = ur"^/%s(\d+)$" % OPEN_COMMAND_KEYWORD
REGEXP_AF = ur"^/%s(\d+)$" % AF_COMMAND_KEYWORD
REGEXP_RF = ur"^/%s(\d+)$" % RF_COMMAND_KEYWORD
REGEXP_CATEGORIES = ur"(?i)( *([Кк]атегории)|(/?categories)( .*)?)$"
REGEXP_FAVORITE = ur"(?i)( *([Ии]збранное)|(/?favorites?))( .*)?$"


LOG_DIR = "logs/"
