import re
from enum import Enum

JAVA_SINGLE_LINE_COMMENT = '//'  # Java single line comment
ELIXIR_SINGLE_LINE_COMMENT = '#'  # Elixir single line comment
RUST_SINGLE_LINE_COMMENT = '//'  # Rust single line comment

ELIXIR_MC_INDICATOR = ["spawn", "spawn_link", "spawn_monitor", "self", "send", "receive", "Agent", "Application",
                       "Config", "Config.Provider", "Config.Reader", "DynamicSupervisor", "GenServer", "Node",
                       "Process", "Registry", "Supervisor", "Task", "Task.Supervisor", "Mix.Config"]

JAVA_MC_INDICATOR = ["Thread"]
RUST_MC_INDICATOR = ["Thread"]


class Language(Enum):
    JAVA = 1
    ELIXIR = 2
    RUST = 3


class ReadDiff:

    def __init__(self, language: Language = Language.JAVA):
        """
        Constructor
        :param language: the language of the code in the diff
        """
        self.linecounter = None
        self.removed_lines = None
        self.new_lines = None
        self.filepath = ""
        self.lines = ""
        match language:
            case Language.JAVA:
                self.single_line_comment = JAVA_SINGLE_LINE_COMMENT
                self.mc_indicators = JAVA_MC_INDICATOR
            case Language.ELIXIR:
                self.single_line_comment = ELIXIR_SINGLE_LINE_COMMENT
                self.mc_indicators = ELIXIR_MC_INDICATOR
            case Language.RUST:
                self.single_line_comment = RUST_SINGLE_LINE_COMMENT
                self.mc_indicators = RUST_MC_INDICATOR

    def __init__(self, language: Language = Language.JAVA, zoeklijst=None):
        """
        Constructor
        :param language: the language of the code in the diff
        """
        if zoeklijst is None:
            zoeklijst = ['Thread']
        self.linecounter = None
        self.removed_lines = None
        self.new_lines = None
        self.filepath = ""
        self.lines = ""
        self.mc_indicators = zoeklijst
        match language.upper():
            case 'JAVA':
                self.single_line_comment = JAVA_SINGLE_LINE_COMMENT
            case 'ELIXIR':
                self.single_line_comment = ELIXIR_SINGLE_LINE_COMMENT
            case 'RUST':
                self.single_line_comment = RUST_SINGLE_LINE_COMMENT


    def read_diff_text(self, chunk=''):
        """
        Read a diff chunk text, and return the new and removed un-empty lines, together with the line number and
        an array of found keywords.
        :param chunk: diff text
        :return: tuple of two lists. The first list contains tuples of (line number, line, [keywords]) of
            (un-empty) new lines. The second list contains tuples of (line number, line, [keywords]) of (un-empty)
            removed lines.
        """
        self.lines = chunk.splitlines()
        if len(self.lines) == 0:
            return [], []
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
        first_at_removed = line[2:]
        split_on_at = [word.strip() for word in first_at_removed.split('@@')]
        split_chunk_parts = [word.strip() for word in split_on_at[0].split(' ')]
        return int(split_chunk_parts[0].split(',')[0][1:]), int(split_chunk_parts[1].split(',')[0][1:])

    def __clean_and_analyse_line(self, line):
        """
        Clean a line of the diff text, and analyse it for keywords
        Removes first character (either + or -), and removes comments.
        :param line: line to clean and analyse
        :return: the line stripped of comments, and first character
        """
        line = line[1:].strip()
        pos_comment = line.find(self.single_line_comment)
        if pos_comment >= 0:
            line = line[:pos_comment]
        if len(line) > 0:
            mc_found = self.__find_all_primitives(line)
        else:
            mc_found = []  # empty line, no code
        return line, mc_found

    def __find_all_primitives(self, line):
        """
        Find all primitives in a line of code, also excludes text within string literals
        :param line: a line stripped of comments and first character
        :return: array containing all primitives found in the line
        """
        mc_found = []
        temp_line = re.sub("\"", " QUOTE ", line)
        # vervang alles dat niet een letter, punt of underscore is door een spatie
        # en split vervolgens op spaties
        words = re.sub("[^a-zA-Z._] ", " ", temp_line).split()
        start_quote_found = False
        for word in words:
            stripped_word = word.strip()
            # check of tekst zich binnen een string literal bevindt
            if not start_quote_found and stripped_word == "QUOTE":
                start_quote_found = True
                continue
            if start_quote_found and stripped_word == "QUOTE":
                start_quote_found = False
            if start_quote_found:
                continue
            if stripped_word in self.mc_indicators:
                mc_found.append(stripped_word)
        return mc_found
