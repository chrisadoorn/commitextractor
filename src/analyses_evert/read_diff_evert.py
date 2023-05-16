import string
from collections import deque

JAVA_IDENTIFIER_GRAMMAR = list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['_', '$'] + list(string.digits)


class ReadDiffEvert:

    def __init__(self, language: str = "JAVA"):
        self.language = language

    def find_key_words(self, text='', text_to_find=''):
        line_list = deque(text)
        instances_found = 0
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                break
            if c == '/':
                c = self.__line_comment(line_list)
                if c is None:
                    break
            if c == '"':
                c = self.__string_literal(line_list)
                if c is None:
                    break
            if c == '*':
                c = self.__end_block_comment(line_list)
                if c is None:
                    break
                if c == '/':
                    instances_found = 0
            if c in JAVA_IDENTIFIER_GRAMMAR:
                w = self.__concat(line_list, c)
                if w == text_to_find:
                    instances_found += 1
        return instances_found

    def __line_comment(self, line_list: deque):
        c = line_list.popleft() if line_list else ''
        if c == '' or c == '/' or c == '*':
            return self.__stop()
        else:
            return c

    def __end_block_comment(self, line_list: deque):
        c = line_list.popleft() if line_list else ''
        if c == '':
            return self.__stop()
        else:
            return c

    def __string_literal(self, line_list: deque):
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return self.__stop()
            if c == '"':
                return c

    def __concat(self, line_list: deque, w: str):
        while True:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return w
            if c not in JAVA_IDENTIFIER_GRAMMAR:
                line_list.appendleft(c)
                return w
            w += c

    @staticmethod
    def __stop():
        return None
