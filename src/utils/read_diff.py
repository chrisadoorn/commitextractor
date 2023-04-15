import logging
import os
import re
from datetime import datetime
from enum import Enum

from src.models.models import pg_db_schema, pg_db

JAVA_SINGLE_LINE_COMMENT = '//'  # Java single line comment
ELIXIR_SINGLE_LINE_COMMENT = '#'  # Elixir single line comment
RUST_SINGLE_LINE_COMMENT = '//'  # Rust single line comment

ELIXIR_MC_INDICATOR = ["spawn",
                       "spawn_link",
                       "spawn_monitor",
                       "self",
                       "send",
                       "receive",
                       "Agent",
                       "Application",
                       "Config",
                       "Config.Provider",
                       "Config.Reader",
                       "DynamicSupervisor",
                       "GenServer",
                       "Node",
                       "Process",
                       "Registry",
                       "Supervisor",
                       "Task",
                       "Task.Supervisor"]

JAVA_MC_INDICATOR = ["Thread"]
RUST_MC_INDICATOR = ["Thread"]

filename = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '..', '..', 'log', 'main.' + str(datetime.now()) + '.log'))


def initialize():
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


class Language(Enum):
    JAVA = 1
    ELIXIR = 2
    RUST = 3


class ReadDiff:

    def __init__(self, language: Language = Language.JAVA):
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

    def read_diff_text(self, chunk=''):
        self.lines = chunk.splitlines()
        if len(self.lines) == 0:
            return "No lines found"
        self.new_lines = []
        self.removed_lines = []
        self.linecounter = (0, 0)
        for line in self.lines:
            self.__process_line(line)

        print("Aantal aangepaste regels: " + str(len(self.new_lines) + len(self.removed_lines)))
        print("Nieuwe regels:")
        for l1 in self.new_lines:
            if l1[2]:
                print(l1)
        print("Verwijderde regels:")
        for l2 in self.removed_lines:
            if l2[2]:
                print(l2)

    def __process_line(self, line):
        if line.startswith('@@'):
            self.linecounter = self.__process_chunk_line(line)
        elif line.startswith('-'):
            (line, is_mc) = self.__clean_diff_line(line)
            if len(line) > 0:
                item = (self.linecounter[0], line, is_mc)
                self.removed_lines.append(item)
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1])
        elif line.startswith('+'):
            (line, is_mc) = self.__clean_diff_line(line)
            if len(line) > 0:
                item = (self.linecounter[1], line, is_mc)
                self.new_lines.append(item)
            self.linecounter = (self.linecounter[0], self.linecounter[1] + 1)
        else:
            self.linecounter = (self.linecounter[0] + 1, self.linecounter[1] + 1)
        print(self.linecounter)

    @staticmethod
    def __process_chunk_line(line):
        first_at_removed = line[2:]
        split_on_at = [word.strip() for word in first_at_removed.split('@@')]
        split_chunk_parts = [word.strip() for word in split_on_at[0].split(' ')]
        return int(split_chunk_parts[0].split(',')[0][1:]), int(split_chunk_parts[1].split(',')[0][1:])

    def __clean_diff_line(self, line):
        pos_comment = line.find(self.single_line_comment)
        if pos_comment > -1:
            line = line[:pos_comment]
        line = line[2:].strip()
        is_mc = self.__is_mc_line(line)
        return line, is_mc

    def __is_mc_line(self, line):
        for mc_indicator in self.mc_indicators:
            r1 = re.search(r'(.*)' + mc_indicator + '(.*)', line, re.U)
            if r1 is not None:
                return True

        return False


if __name__ == '__main__':
    try:
        limit = 100_000
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        schema = pg_db_schema
        read_diff = ReadDiff(language=Language.ELIXIR)
        sql = \
            "select bw.id, bw.idcommit, bw.locatie, bw.filename, bw.difftext from " + schema + \
            ".bestandswijziging as bw where difftext is not null limit({});".format(limit) \
            if limit is not None else \
            "select bw.id, bw.idcommit, bw.locatie, bw.filename, bw.difftext from " + schema + \
            ".bestandswijziging as bw where difftext is not null;"

        cursor = pg_db.execute_sql(sql)
        counter = 1
        for (bestandswijziging_id, id_commit, locatie, filename, diff_text) in cursor.fetchall():
            print("counter: " + str(counter))
            print("id: " + str(bestandswijziging_id))
            print("filename: " + filename)
            read_diff.read_diff_text(diff_text)
            print("--------------------")
            counter += 1

        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
