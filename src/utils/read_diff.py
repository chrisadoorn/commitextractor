import string
from collections import deque


class InvalidDiffText(Exception):
    """Raised when the diff text is not valid"""
    pass


class _FindKeyWordsInterface:
    identifier_alphabet = ""

    def find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
        pass

    def line_comment(self, c, line_list: deque) -> str | None:
        next_c = line_list.popleft() if line_list else ''
        if next_c == '' or next_c == '/' or next_c == '*':
            return self.stop()
        else:
            line_list.appendleft(next_c)
            return c

    def end_block_comment(self, line_list: deque) -> str | None:
        c = line_list.popleft() if line_list else ''
        if c == '':
            return self.stop()
        else:
            return c

    def double_quote_literal(self, line_list: deque) -> str | None:
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return self.stop()
            if c == '"':
                return c

    def single_quote_literal(self, line_list: deque) -> str | None:
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return self.stop()
            if c == '\'':
                return c

    def concat(self, line_list: deque, w: str) -> str:
        while True:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return w
            if c not in self.identifier_alphabet:
                line_list.appendleft(c)  # put back the character for the next iteration
                return w
            w += c

    @staticmethod
    def stop() -> None:
        return None


class _ReadDiff(object):

    def __init__(self, find_key_words_interface: _FindKeyWordsInterface):
        """
        Constructor
        """
        self.linecounter = None
        self.removed_lines = None
        self.new_lines = None
        self.lines = ""
        self.find_key_words = find_key_words_interface

    def check_diff_text(self, chunk: str = '', words: list[str] = None) -> tuple[
        list[tuple[int, str, set[str]]], list[tuple[int, str, set[str]]]]:

        """
        Read a diff chunk text, and return the new- and removed (un-empty) lines, together with the line number and
        a set of found keywords.
        The new lines are compared with the old lines, A new line contains a word if that word occurs more in the
        new line then in the old line.
        :param words: words to look for
        :param chunk: diff text
        :return: tuple of two lists. The first list contains tuples of (line number, line, set([keywords])) of
        (un-empty) new lines. The second list contains tuples of (line number, line, set([keywords])) of (un-empty)
        removed lines.
        """
        self.check_diff_text_no_check_with_removed(chunk, words)
        self.__check_with_removed_lines()
        return self.new_lines, self.removed_lines

    def check_diff_text_no_check_with_removed(self, chunk: str = '', words: list[str] = None) -> tuple[
        list[tuple[int, str, set[str]]], list[tuple[int, str, set[str]]]]:
        """
        Read a diff chunk text, and return the new and removed un-empty lines, together with the line number and
        an array of found keywords.
        :param words: words to look for
        :param chunk: diff text
        :return: tuple of two lists. The first list contains tuples of (line number, line, [keywords]) of
            (un-empty) new lines. The second list contains tuples of (line number, line, [keywords]) of (un-empty)
            removed lines.
        """
        if words is None or len(words) == 0:
            return [], []
        if chunk is None or len(chunk) == 0:
            return [], []
        self.lines = chunk.splitlines()
        if len(self.lines) == 0:
            return [], []
        if not self.lines[0].startswith('@@'):
            raise InvalidDiffText('Text no valid diff text')
        self.new_lines = []
        self.removed_lines = []
        self.linecounter = (0, 0)
        for line in self.lines:
            self.__process_line(line, words)
        return self.new_lines, self.removed_lines

    def __check_with_removed_lines(self) -> None:
        temp_lines = []
        for new_lnr, new_line, new_keys in self.new_lines:
            self.__loop_through_removed_line(new_lnr, new_keys)
            temp_lines.append((new_lnr, new_line, set(new_keys)))  # remove duplicates by creating a set
        self.new_lines = temp_lines
        temp_lines = []
        for rem_lnr, rem_line, rem_keys in self.removed_lines:
            temp_lines.append((rem_lnr, rem_line, set(rem_keys)))  # remove duplicates by creating a set
        self.removed_lines = temp_lines

    def __loop_through_removed_line(self, l_nr: int, new_keys: list[str]):
        """
        Check for occurrence of a keyword on the same line in the removed_lines and new_lines.
        The new_line, after this method, contains the added keywords minus the keywords from the removed_line.
        This because when a keyword is added and removed on the same line there is no change.
        :param l_nr: line number
        :param new_keys: list of keywords found on the line
        :return: none, but the new_keys is changed
        """
        for rem_lnr, rem_line, rem_keys in self.removed_lines:
            if rem_lnr == l_nr:
                new_temp_keys = new_keys.copy()
                rem_temp_keys = rem_keys.copy()
                for key in new_temp_keys:
                    if key in rem_temp_keys:
                        new_keys.remove(key)
                        rem_temp_keys.remove(key)

    def __process_line(self, line: str, words: list[str]) -> None:
        """
        Process one line of the diff text
        :param line: the line to process
        """
        if line.startswith('@@'):
            self.linecounter = self.__process_chunk_line(line)
        elif line.startswith('-'):
            (line, mc_count) = self.__clean_and_analyse_line(line, words)
            if len(line) > 0:
                item = (self.linecounter[0], line, mc_count)
                self.removed_lines.append(item)
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1])
        elif line.startswith('+'):
            (line, mc_count) = self.__clean_and_analyse_line(line, words)
            if len(line) > 0:
                item = (self.linecounter[1], line, mc_count)
                self.new_lines.append(item)
            self.linecounter = (self.linecounter[0], self.linecounter[1] + 1)
        else:
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1] + 1)

    @staticmethod
    def __process_chunk_line(line: str) -> tuple[int, int]:
        """
        Process a chunk line (a line starting with '@@')
        :param line: a line starting with '@@'
        :return: tuple of two integers. The first integer is the start line number of old file (-), the other
                 integer start line of the new file (+).
        """
        if not line.startswith('@@'):
            raise InvalidDiffText('Text no valid diff text, missing start @@')
        first_at_removed = line[2:]
        if first_at_removed.find('@@') < 0:
            raise InvalidDiffText('Text no valid diff text, missing end @@')
        split_on_at = [word.strip() for word in first_at_removed.split('@@')]
        split_chunk_parts = [word.strip() for word in split_on_at[0].split(' ')]
        try:
            if split_chunk_parts[0][0] != '-' or split_chunk_parts[1][0] != '+':
                raise InvalidDiffText('Text no valid diff text')
            return int(split_chunk_parts[0].split(',')[0][1:]), int(split_chunk_parts[1].split(',')[0][1:])
        except IndexError or ValueError:
            raise InvalidDiffText('Text no valid diff text, could not determine line numbers')

    def __clean_and_analyse_line(self, line: str, words: list[str] = None) -> tuple[str, list[str]]:
        """
        Clean a line of the diff text, and analyse it for keywords
        Removes first character (either + or -), and removes comments.
        :param line: line to clean and analyse
        :return: the line stripped of comments, and first character
        """
        mc_list = []
        if line.startswith('-') or line.startswith('+'):
            line = line[1:].strip()
            if len(line) > 0:
                mc_list = self.find_key_words.find_key_words(line, words)
        return line, mc_list


class ReadDiffJava(_ReadDiff):

    def __init__(self):
        super().__init__(self.__FindKeyWords())

    class __FindKeyWords(_FindKeyWordsInterface):
        # This list consist of characters allowed in the words we wou are looking for.
        identifier_alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['_',
                                                                                                                   '$']

        def find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
            line_list = deque(text)
            instances_found = []
            while line_list:
                c = line_list.popleft() if line_list else ''
                if c == '':
                    break

                if c == '/':
                    if self.line_comment(c, line_list) is None:
                        break
                    continue

                if c == '*':
                    c = self.end_block_comment(line_list)
                    if c is None:
                        break
                    if c == '/':
                        instances_found = []

                if c == '"':
                    if self.double_quote_literal(line_list) is None:
                        break
                    continue

                if c == '\'':
                    if self.single_quote_literal(line_list) is None:
                        break
                    continue

                if c is None:
                    break

                if c in self.identifier_alphabet:
                    w = self.concat(line_list, c)
                    if w in text_to_find:
                        instances_found.append(w)
            return instances_found


class ReadDiffElixir(_ReadDiff):

    def __init__(self):
        super().__init__(self.__FindKeyWords())

    class __FindKeyWords(_FindKeyWordsInterface):
        identifier_alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['_', '.']

        def find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
            line_list = deque(text)
            instances_found = []
            while line_list:
                c = line_list.popleft() if line_list else ''
                if c == '':
                    break

                if c == '#':
                    break

                if c == '~':
                    if self.sigil(c, line_list) is None:
                        break
                    continue

                if c == '"':
                    if self.double_quote_literal(line_list) is None:
                        break
                    continue

                if c == '\'':
                    if self.single_quote_literal(line_list) is None:
                        break
                    continue

                if c is None:
                    break

                if c in self.identifier_alphabet:
                    w = self.concat(line_list, c)
                    if w in text_to_find:
                        instances_found.append(w)
            return instances_found

        def sigil(self, c, line_list: deque) -> str | None:
            next_c = line_list.popleft() if line_list else ''
            if next_c == '':
                return self.stop()
            if next_c not in ['c', 'C', 's', 'S']:
                line_list.appendleft(next_c)  # put back the character,so it can be popped again in the next iteration
                return c
            double_next_c = line_list.popleft() if line_list else ''
            if double_next_c == '' or double_next_c not in ['(', '{']:
                line_list.appendleft(double_next_c)  # put back the character for the next iteration
                line_list.appendleft(next_c)  # put back the character for the next iteration
                return c
            while line_list:
                triple_next_c = line_list.popleft() if line_list else ''
                if triple_next_c == '':
                    return self.stop()
                if double_next_c == '(' and triple_next_c == ')' or double_next_c == '{' and triple_next_c == '}':
                    return double_next_c


class ReadDiffRust(_ReadDiff):

    def __init__(self):
        super().__init__(self.__FindKeyWords())

    class __FindKeyWords(_FindKeyWordsInterface):
        # This list consist of characters allowed in the words we wou are looking for.
        identifier_alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['_',
                                                                                                                   '$']

        def find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
            line_list = deque(text)
            instances_found = []
            while line_list:
                c = line_list.popleft() if line_list else ''
                if c == '':
                    break

                if c == '/':
                    if self.line_comment(c, line_list) is None:
                        break
                    continue

                if c == '*':
                    c = self.end_block_comment(line_list)
                    if c is None:
                        break
                    if c == '/':
                        instances_found = []

                if c == '"':
                    if self.double_quote_literal(line_list) is None:
                        break
                    continue

                if c == '\'':
                    if self.single_quote_literal(line_list) is None:
                        break
                    continue

                if c is None:
                    break

                if c in self.identifier_alphabet:
                    w = self.concat(line_list, c)
                    if w in text_to_find:
                        instances_found.append(w)
            return instances_found