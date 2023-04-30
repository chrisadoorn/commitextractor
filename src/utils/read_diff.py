import re

JAVA_SINGLE_LINE_COMMENT = '//'  # Java single line comment
JAVA_MULTI_LINE_COMMENT_START = r'/\*'  # Java single line comment
JAVA_MULTI_LINE_COMMENT_END = r'\*/'  # Java single line comment
ELIXIR_SINGLE_LINE_COMMENT = '#'  # Elixir single line comment
RUST_SINGLE_LINE_COMMENT = '//'  # Rust single line comment
RUST_MULTI_LINE_COMMENT_START = r'/\*'  # Rust single line comment
RUST_MULTI_LINE_COMMENT_STOP = r'\*/'  # Rust single line comment
STRING_QUOTE = '"'  # String quote, luckily same for all languages,
CHAR_QUOTE = '\''  # Char quote, luckily same for all 3 languages,

ELIXIR_MC_INDICATOR = ["spawn", "spawn_link", "spawn_monitor", "send", "self", "receive", "flush" "Agent.",
                       "GenServer", "Node", "Process", "Supervisor", "Task"]

JAVA_MC_INDICATOR = ["Thread"]
RUST_MC_INDICATOR = ["Thread"]


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
        match language.upper():
            case "JAVA":
                self.single_line_comment = JAVA_SINGLE_LINE_COMMENT
                self.mc_indicators = JAVA_MC_INDICATOR if zoeklijst is None else zoeklijst
                self.multi_line_comment_start = JAVA_MULTI_LINE_COMMENT_START
                self.multi_line_comment_end = JAVA_MULTI_LINE_COMMENT_END
            case "ELIXIR":
                self.single_line_comment = ELIXIR_SINGLE_LINE_COMMENT
                self.mc_indicators = ELIXIR_MC_INDICATOR if zoeklijst is None else zoeklijst
            case "RUST":
                self.single_line_comment = RUST_SINGLE_LINE_COMMENT
                self.mc_indicators = RUST_MC_INDICATOR if zoeklijst is None else zoeklijst
                self.multi_line_comment_start = JAVA_MULTI_LINE_COMMENT_START
                self.multi_line_comment_end = JAVA_MULTI_LINE_COMMENT_END

        self.KEEP_CHARS = r"[^a-zA-Z_/\*#\\'\"]"

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
                mc_found = self.__find_all_primitives(line)
            else:
                mc_found = []  # empty line, no code
            return line, mc_found
        else:
            return line, []

    def __find_all_primitives(self, line):
        """
        Find all primitives in a line of code, also excludes text within string literals
        Per line of text.
        :param line: a line stripped of comments and first character
        :return: array containing all primitives found in the line
        """
        mc_found = []
        temp_line = re.sub(STRING_QUOTE, " " + STRING_QUOTE + " ", line)
        temp_line = re.sub(CHAR_QUOTE, " " + CHAR_QUOTE + " ", temp_line)
        if self.multi_line_comment_start is not None:
            temp_line = re.sub(self.multi_line_comment_start, " " + self.multi_line_comment_start + " ", temp_line)
        if self.multi_line_comment_end is not None:
            temp_line = re.sub(self.multi_line_comment_end, " " + self.multi_line_comment_end + " ", temp_line)
        temp_line = re.sub(self.single_line_comment, " " + self.single_line_comment + " ", temp_line)
        # vervang alles dat niet een letter, punt of underscore is door een spatie
        # en split vervolgens op spaties
        temp_line = re.sub(self.KEEP_CHARS, " ", temp_line)
        start_quote_found = False
        for word in temp_line.split():
            stripped_word = word.strip()
            if not start_quote_found and (stripped_word == STRING_QUOTE or stripped_word == CHAR_QUOTE):
                start_quote_found = True
                continue  # begin string literal, volgende woorden kunnen geen keywords zijn
            if start_quote_found and (stripped_word == STRING_QUOTE or stripped_word == CHAR_QUOTE):
                start_quote_found = False  # einde string literal, volgende woorden kunnen weer keywords zijn
            if start_quote_found:
                continue  # binnen string literal
            if stripped_word == self.single_line_comment or stripped_word == self.multi_line_comment_start:
                break  # alles hierna is commentaar, verder zoeken is niet nodig
            if stripped_word == self.multi_line_comment_end:
                mc_found = []  # alles hiervoor stond in een multiline comment, dus geen mc's gevonden, hierna  # kunnen wel weer keywords voorkomen
            if stripped_word not in mc_found and stripped_word in self.mc_indicators:
                mc_found.append(stripped_word)
        return mc_found
