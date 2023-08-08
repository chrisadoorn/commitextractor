import logging
import string

from src.models.analyzed_data_models import Zoekterm
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration
from src.models.extracted_data_models import BestandsWijziging
from src.utils import db_postgresql, configurator
from src.utils.read_diff import ReadDiffRust, ReadDiffElixir
from collections import deque

global db_connectie
schema = get_database_configuration().get('schema')















zoekterm_list = []
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
        self.find_key_words_interface = find_key_words_interface

    def check_diff_text(self, chunk: str = '', words: list[str] = None) -> tuple[
            list[tuple[int, str, list[str]]], list[tuple[int, str, list[str]]]]:
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
                mc_list = self.find_key_words_interface.find_key_words(line, words)
        return line, mc_list

"""_ReadDiff als parameter dus dit wordt de parent class"""
class ReadDiffRust(_ReadDiff):

    """init wordt automatisch opgeroepen als er een instantie wordt aangemaakt"""
    def __init__(self):
        print("init")
        super().__init__(self.__FindKeyWords())

    class __FindKeyWords(_FindKeyWordsInterface):
        print("class __FindKeyWords")
        # This list consist of characters allowed in the words we are looking for.
        identifier_alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['-','_',':','::']


        """
        Rust contains line comments starting with //, doc comments starting with /// or //! and      
        multi-line  comments starting with /* and ending with */
        Rust contains single and double quote literals
        """
        def find_key_words(self, text: str = '', text_to_find: list[str] = None) -> list[str]:
            print("Nu find_key_words")
            line_list = deque(text)
            print("line_list " + str(line_list))
            instances_found = []
            while line_list:
                c = line_list.popleft() if line_list else ''
                if c == '':
                    break

                if c == '/':
                    print("line_comment " + str(line_list))
                    if self.line_comment(c, line_list) is None:
                        break
                    continue

                if c == '*':
                    print("end_block_comment " + str(line_list))
                    c = self.end_block_comment(line_list)
                    if c is None:
                        break
                    if c == '/':
                        instances_found = []

                if c == '"':
                    print("double_quote_literal " + str(line_list))
                    if self.double_quote_literal(line_list) is None:
                        break
                    continue

                if c == '\'':
                    print("single_quote_literal " + str(line_list))
                    if self.single_quote_literal(line_list) is None:
                        break
                    continue

                if c is None:
                    break

                if c in self.identifier_alphabet:
                    print("concat " + str(line_list))
                    w = self.concat(line_list, c)
                    if w[:11] == "std::thread":
                        w = w[:11]
                    if w[:17] == "std::marker::sync":
                        w = w[:17]
                    if w[:17] == "std::marker::Send":
                        w = w[:17]
                    print("text_to_find " + str(text_to_find))
                    print ("Ascii?  " + str(str(text_to_find).isascii()))
                    print("w " + str(w))
                    if w in text_to_find:
                        print("append " + str(w))
                        instances_found.append(w)
            return instances_found

    @staticmethod
    def read_diff_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk

if __name__ == '__main__':
    read_diff = ReadDiffRust()
    keywords = ["std::thread"]
    diff_text = read_diff.read_diff_file(filepath='./read_diff_rust_test.txt')
    (new_lines, old_lines) = read_diff.check_diff_text(diff_text, keywords)
    print("new_lines" + str(new_lines))
    print("old_lines" + str(old_lines))












































def __get_bestandswijzigingen_list():
    """
    retrieves the list of bestandswijzigingen for a project containing a certain keyword.
    :param zoekterm: Zoekterm object
    :param project_id:
    :return: List of tuples, the first element containing the id of a bestandswijzigng
    """
    language = configurator.get_main_language()[0]
    if language.upper() == 'RUST':
        print("optimising rust Toml files")
        __optimizing_toml_rust_files()

def __optimizing_toml_rust_files ():
    """
    retrieves the list of bestandswijzigingen of .toml files for a project, reduces it to library-dependencies
    :return: updates difftest, tekstvooraf, tekstachteraf in table bestandswijzigng
    """
    for bestandswijziging in BestandsWijziging.select().where(BestandsWijziging.extensie == '.toml' and BestandsWijziging.idcommit == '78'):
        if bestandswijziging.difftext is not None:
            print("bestandswijziging.difftext\n" + bestandswijziging.difftext)
            print("opkuis bestandswijziging.difftext\n " + ReadDiffRust.clean_rust_toml(bestandswijziging.difftext))
            bestandswijziging.difftext = ReadDiffRust.clean_rust_toml(bestandswijziging.difftext)

        if bestandswijziging.tekstachteraf is not None:
            print("bestandswijziging.tekstachteraf\n " + str(bestandswijziging.tekstachteraf))
            print("opkuis bestandswijziging.tekstachteraf\n " + ReadDiffRust.clean_rust_toml(bestandswijziging.tekstachteraf))
            bestandswijziging.tekstachteraf = ReadDiffRust.clean_rust_toml(bestandswijziging.tekstachteraf)

        if bestandswijziging.tekstvooraf is not None:
            print("bestandswijziging.tekstvooraf\n " + str(bestandswijziging.tekstvooraf))
            print("opkuis bestandswijziging.tekstvooraf\n " + ReadDiffRust.clean_rust_toml(bestandswijziging.tekstvooraf))
            bestandswijziging.tekstvooraf = ReadDiffRust.clean_rust_toml(bestandswijziging.tekstvooraf)