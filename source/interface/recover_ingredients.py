# -*- coding: utf-8 -*-


class recover_automat:
    def comment(self, char):
        if char == '(':
            self.deep += 1
        elif char == ')':
            self.deep -= 1
            if self.deep == 0:
                self.statement = self.prev_statement

    def string(self, char):
        if char == '(':
            self.deep = 1
            self.statement = self.comment
            self.prev_statement = self.string
        elif char.isdigit():
            self.statement = self.number
            return '\n'

    def number(self, char):
        if char == '(':
            self.deep = 1
            self.statement = self.comment
            self.prev_statement = self.number
        elif char.isalpha():
            self.statement = self.string

    def __init__(self):
        self.deep = 0
        self.statement = self.number
        self.prev_statement = None


def recover(text):
    for line in text:
        robot = recover_automat()
        recovered_line = ""
        for char in line:
            if robot.statement(char) is not None:
                yield recovered_line
                recovered_line = ""
            recovered_line += char
        yield recovered_line
