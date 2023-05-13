import string
from collections import deque

ELIXIR_MC_INDICATOR = ["spawn", "spawn_link", "spawn_monitor", "send", "self", "receive", "flush" "Agent", "GenServer",
                       "Node", "Process", "Supervisor", "Task"]

JAVA_MC_INDICATOR = ["Thread"]
RUST_MC_INDICATOR = ["Thread"]

JAVA_IDENTIFIER_GRAMMAR = list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['_', '$'] + [str(i) for i in
                                                                                                      list(
                                                                                                          range(0, 10))]


class InvalidDiffText(Exception):
    """Raised when the diff text is not valid"""
    pass


class ReadDiff:

    def __init__(self, language: str = "JAVA", zoeklijst: list[str] = None):
        """
        Constructor
        :param language: the language of the code in the diff
        """
        self.linecounter = None
        self.removed_lines = None
        self.new_lines = None
        self.filepath = ""
        self.lines = ""
        self.multi_line_comment_start = None
        self.multi_line_comment_end = None
        self.language = language.upper()
        match language.upper():
            case "JAVA":
                self.mc_indicators = JAVA_MC_INDICATOR if zoeklijst is None else zoeklijst
            case "ELIXIR":
                self.mc_indicators = ELIXIR_MC_INDICATOR if zoeklijst is None else zoeklijst
            case "RUST":
                self.mc_indicators = RUST_MC_INDICATOR if zoeklijst is None else zoeklijst

    def read_diff_text(self, chunk=''):
        """
        Read a diff chunk text, and return the new and removed un-empty lines, together with the line number and
        an array of found keywords.
        :param chunk: diff text
        :return: tuple of two lists. The first list contains tuples of (line number, line, [keywords]) of
            (un-empty) new lines. The second list contains tuples of (line number, line, [keywords]) of (un-empty)
            removed lines.
        """
        if chunk is None:
            return None
        self.lines = chunk.splitlines()
        if len(self.lines) == 0:
            return [], []
        if not self.lines[0].startswith('@@'):
            raise InvalidDiffText('Text no valid diff text')
        self.new_lines = []
        self.removed_lines = []
        self.linecounter = (0, 0)
        for line in self.lines:
            self.__process_line(line)
        self.__check_with_removed_lines()
        return self.new_lines, self.removed_lines

    def __check_with_removed_lines(self):
        for new_lnr, new_line, new_keys in self.new_lines:
            for rem_lnr, rem_line, rem_keys in self.removed_lines:
                if new_lnr == rem_lnr:
                    new_temp_keys = new_keys.copy()
                    for key in new_temp_keys:
                        if key in rem_keys:
                            new_keys.remove(key)

    def check_diff_text_on_word(self, chunk='', word=''):
        """
        Read a diff chunk text, and return the new and removed un-empty lines, together with the line number and
        an array of found keywords.
        :param word:
        :param chunk: diff text
        :return: tuple of two lists. The first list contains tuples of (line number, line, [keywords]) of
            (un-empty) new lines. The second list contains tuples of (line number, line, [keywords]) of (un-empty)
            removed lines.
        """
        if chunk is None:
            return None
        self.lines = chunk.splitlines()
        if len(self.lines) == 0:
            return [], []
        if not self.lines[0].startswith('@@'):
            raise InvalidDiffText('Text no valid diff text')
        self.new_lines = []
        self.removed_lines = []
        self.linecounter = (0, 0)
        for line in self.lines:
            self.__process_line_word(line, word)
        self.__check_with_removed_lines()
        return self.new_lines, self.removed_lines

    def __process_line(self, line) -> None:
        """
        Process one line of the diff text
        :param line: the line to process
        """
        if line.startswith('@@'):
            self.linecounter = self.__process_chunk_line(line)
        elif line.startswith('-'):
            (line, is_mc) = self.__clean_and_analyse_line(line)
            if len(line) > 0:
                item = (self.linecounter[0], line, is_mc)
                self.removed_lines.append(item)
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1])
        elif line.startswith('+'):
            (line, is_mc) = self.__clean_and_analyse_line(line)
            if len(line) > 0:
                item = (self.linecounter[1], line, is_mc)
                self.new_lines.append(item)
            self.linecounter = (self.linecounter[0], self.linecounter[1] + 1)
        else:
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1] + 1)

    def __process_line_word(self, line, word) -> None:
        """
        Process one line of the diff text
        :param line: the line to process
        """
        if line.startswith('@@'):
            self.linecounter = self.__process_chunk_line(line)
        elif line.startswith('-'):
            (line, is_mc) = self.__clean_and_analyse_line_word(line, word)
            if len(line) > 0:
                item = (self.linecounter[0], line, is_mc)
                self.removed_lines.append(item)
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1])
        elif line.startswith('+'):
            (line, is_mc) = self.__clean_and_analyse_line_word(line, word)
            if len(line) > 0:
                item = (self.linecounter[1], line, is_mc)
                self.new_lines.append(item)
            self.linecounter = (self.linecounter[0], self.linecounter[1] + 1)
        else:
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1] + 1)

    @staticmethod
    def __process_chunk_line(line):
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

    def __clean_and_analyse_line(self, line):
        """
        Clean a line of the diff text, and analyse it for keywords
        Removes first character (either + or -), and removes comments.
        :param line: line to clean and analyse
        :return: the line stripped of comments, and first character
        """
        if line.startswith('-') or line.startswith('+'):
            line = line[1:].strip()
            if len(line) > 0:
                if self.language == "JAVA" or self.language == "RUST":
                    mc_found = self.__find_all_identifiers_java(line)
                else:
                    mc_found = self.__find_all_identifiers_elixir(line)
            else:
                mc_found = []  # empty line, no code
            return line, mc_found
        else:
            return line, []

    def __clean_and_analyse_line_word(self, line, word):
        """
        Clean a line of the diff text, and analyse it for keywords
        Removes first character (either + or -), and removes comments.
        :param line: line to clean and analyse
        :return: the line stripped of comments, and first character
        """
        if line.startswith('-') or line.startswith('+'):
            line = line[1:].strip()
            if len(line) > 0:
                if self.language == "JAVA" or self.language == "RUST":
                    mc_found = self.__find_key_word(line, word)
                else:
                    mc_found = self.__find_key_word(line, word)
            else:
                mc_found = []  # empty line, no code
            return line, mc_found
        else:
            return line, []

    def __find_all_identifiers_java(self, text: str):
        """
        Find all identifiers in a line of java text
        :param text: 
        :return:
        """
        start_word = False
        word = ""
        mc_found = []
        string_literal_found = False
        start_comment_found = False
        end_comment_found = False
        for c in list(text):
            if c == '"':
                if string_literal_found:
                    string_literal_found = False
                else:
                    string_literal_found = True
            if string_literal_found:
                continue

            if c == '/':
                if start_comment_found:
                    break
                elif end_comment_found:
                    end_comment_found = False
                    mc_found = []
                    continue
                else:
                    start_comment_found = True
                    continue

            if c == '*':
                if start_comment_found:
                    break
                else:
                    end_comment_found = True
                    continue

            start_comment_found = False
            if c in JAVA_IDENTIFIER_GRAMMAR:
                word += c
                start_word = True
            else:
                if start_word:
                    start_word = False
                    if word not in mc_found and word in self.mc_indicators:
                        mc_found.append(word)
                    word = ""
        if start_word:
            if word not in mc_found and word in self.mc_indicators:
                mc_found.append(word)
        return mc_found

    def __find_all_identifiers_elixir(self, text: str):
        """
        Find all identifiers in a line of elixir text
        :param text:
        :return:
        """
        start_word = False
        word = ""
        mc_found = []
        string_literal_found = False
        for c in list(text):
            if c == '"':
                if string_literal_found:
                    string_literal_found = False
                else:
                    string_literal_found = True
            if string_literal_found:
                continue

            if c == '#':
                break

            if c in JAVA_IDENTIFIER_GRAMMAR:
                word += c
                start_word = True
            else:
                if start_word:
                    start_word = False
                    if word not in mc_found and word in self.mc_indicators:
                        mc_found.append(word)
                    word = ""
        if start_word:
            if word not in mc_found and word in self.mc_indicators:
                mc_found.append(word)
        return mc_found

    def __find_key_word(self, text: str, text_to_find: str):
        if not text or not text_to_find:
            return False
        if text_to_find not in text:
            return False
        line_list = deque(text)
        text_to_find_deque = deque(text_to_find)
        text_found = False
        while line_list:
            c = line_list.popleft() if line_list else None
            c_next = line_list[0] if line_list else ''
            if c == '"':
                self.__handle_string_literal(line_list)
                continue
            if c + c_next == '//' or c + c_next == '/*':
                break  # comment, stop searching
            if c + c_next == '*/':
                text_to_find_deque = deque(text_to_find)
                text_found = False
                continue  # end of comment, continue searching
            if not text_found:
                c_to_compare = text_to_find_deque.popleft()
                if c == c_to_compare and (
                        c_next == '' or c_next not in JAVA_IDENTIFIER_GRAMMAR) and not text_to_find_deque:
                    text_found = True
                    continue
                if c != c_to_compare or (
                        c == c_to_compare and c_next in JAVA_IDENTIFIER_GRAMMAR and not text_to_find_deque):
                    text_to_find_deque = deque(text_to_find)

        return text_found

    @staticmethod
    def __handle_string_literal(line: deque):
        while line:
            c = line.popleft()
            if c == '"':
                break
