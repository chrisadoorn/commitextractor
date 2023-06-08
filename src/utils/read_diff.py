import string
from collections import deque


class InvalidDiffText(Exception):
    """Raised when the diff text is not valid"""
    pass


class ReadDiff:

    def __init__(self, language: str, identifier_grammar: list[str]):
        """
        Constructor
        :param language: the language of the code in the diff
        """
        self.linecounter = None
        self.removed_lines = None
        self.new_lines = None
        self.lines = ""
        self.language = language.upper()
        self.identifier_grammar = identifier_grammar

    def check_diff_text(self, chunk: str = '', words: list[str] = None) -> tuple[
        list[tuple[int, str, set[str]]], list[tuple[int, str, set[str]]]]:
        self.check_diff_text_no_check_with_removed(chunk, words)
        self.__check_with_removed_lines()
        return self.new_lines, self.removed_lines

    def check_diff_text_no_check_with_removed(self, chunk: str = '', words: list[str] = None) -> tuple[
        list[tuple[int, str, set[str]]], list[tuple[int, str, set[str]]]]:
        """
        Read a diff chunk text, and return the new and removed un-empty lines, together with the line number and
        an array of found keywords.
        :param words:
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
            temp_lines.append((new_lnr, new_line, set(new_keys)))
        self.new_lines = temp_lines
        temp_lines = []
        for rem_lnr, rem_line, rem_keys in self.removed_lines:
            temp_lines.append((rem_lnr, rem_line, set(rem_keys)))
        self.removed_lines = temp_lines

    def __loop_through_removed_line(self, l_nr: int, new_keys: list[str]):
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
                mc_list = self.__find_key_words(line, words)
        return line, mc_list

    def __find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
        line_list = deque(text)
        instances_found = []
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                break

            if c == '#' and self.language == "ELIXIR":
                break
            else:
                if c == '/':
                    c = self.__line_comment(line_list)
                    if c is None:
                        break

                if c == '*':
                    c = self.__end_block_comment(line_list)
                    if c is None:
                        break
                    if c == '/':
                        instances_found = []

                if c == '"':
                    c = self.__string_literal(line_list)

                if c == '\'':
                    c = self.__single_quote_literal(line_list)

            if c is None:
                break

            if c in self.identifier_grammar:
                w = self.__concat(line_list, c)
                if w in text_to_find:
                    instances_found.append(w)
        return instances_found

    def __line_comment(self, line_list: deque) -> str | None:
        c = line_list.popleft() if line_list else ''
        if c == '' or c == '/' or c == '*':
            return self.__stop()
        else:
            return c

    def __end_block_comment(self, line_list: deque) -> str | None:
        c = line_list.popleft() if line_list else ''
        if c == '':
            return self.__stop()
        else:
            return c

    def __string_literal(self, line_list: deque) -> str | None:
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return self.__stop()
            if c == '"':
                return c

    def __single_quote_literal(self, line_list: deque) -> str | None:
        while line_list:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return self.__stop()
            if c == '\'':
                return c

    def __concat(self, line_list: deque, w: str) -> str:
        while True:
            c = line_list.popleft() if line_list else ''
            if c == '':
                return w
            if c not in self.identifier_grammar:
                line_list.appendleft(c)
                return w
            w += c

    @staticmethod
    def __stop() -> None:
        return None


class ReadDiffJava(ReadDiff):
    def __init__(self):
        super().__init__("Java",
                         list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['_', '$'])


class ReadDiffElixir(ReadDiff):
    def __init__(self):
        super().__init__("Elixir", list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['_', '.'])

