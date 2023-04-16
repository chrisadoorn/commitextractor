import logging
import os
import re
from peewee import *
from datetime import datetime
from enum import Enum

from src.models.models import pg_db_schema, pg_db, TempDiffTextAnalysis

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
                       "Task.Supervisor", "Mix.Config"]

JAVA_MC_INDICATOR = ["Thread"]
RUST_MC_INDICATOR = ["Thread"]


def initialize():
    logging.basicConfig(filename=os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                               '..', '..', 'log',
                                                               'main.' + str(datetime.now()) + '.log')),
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def create_tables():
    pg_db.create_tables([TempDiffTextAnalysis], safe=True)


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

    def __process_line(self, line):
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
        first_at_removed = line[2:]
        split_on_at = [word.strip() for word in first_at_removed.split('@@')]
        split_chunk_parts = [word.strip() for word in split_on_at[0].split(' ')]
        return int(split_chunk_parts[0].split(',')[0][1:]), int(split_chunk_parts[1].split(',')[0][1:])

    def __clean_and_analyse_line(self, line):
        pos_comment = line.find(self.single_line_comment)
        if pos_comment > -1:
            line = line[:pos_comment]
        line = line[2:].strip()
        mc_found = self.__find_all_primitives(line)
        return line, mc_found

    def __find_all_primitives(self, line):
        mc_found = []
        temp_line = re.sub("\"", " QUOTE ", line)
        words = re.sub("[^a-zA-Z._] ", " ", temp_line).split()
        start_quote_found = False
        for word in words:
            stripped_word = word.strip()
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


def save_temp_diff_text_analysis(bestandswijzigingid, file_name, location, line_number, line_text, primitives,
                                 type_of_diff, author_id, project_name, commitdatumtijd):
    if TempDiffTextAnalysis.select().where(TempDiffTextAnalysis.idbestandswijziging == bestandswijzigingid,
                                           TempDiffTextAnalysis.line_number == line_number).exists():
        return

    temp_diff_text_analysis = TempDiffTextAnalysis()
    temp_diff_text_analysis.idbestandswijziging = bestandswijzigingid
    temp_diff_text_analysis.filename = file_name
    temp_diff_text_analysis.location = location
    temp_diff_text_analysis.line_number = line_number
    temp_diff_text_analysis.line_text = line_text
    temp_diff_text_analysis.primitives = primitives
    temp_diff_text_analysis.type_of_diff = type_of_diff
    temp_diff_text_analysis.project_name = project_name
    temp_diff_text_analysis.author_id = author_id
    temp_diff_text_analysis.commitdatumtijd = commitdatumtijd
    temp_diff_text_analysis.save()


def list_to_string(s):
    str1 = ""
    i = 0
    x = len(s)
    for ele in s:
        if 0 < i < x:
            str1 += ","
        str1 += ele
        i += 1
    return str1


if __name__ == '__main__':
    try:
        limit = 1000
        initialize()
        create_tables()
        logging.info('Started at:' + str(datetime.now()))
        schema = pg_db_schema

        result = TempDiffTextAnalysis.select(fn.MAX(TempDiffTextAnalysis.idbestandswijziging)).scalar()

        if result is None:
            result = 0

        read_diff = ReadDiff(language=Language.ELIXIR)
        sql = \
            "select bw.id, bw.idcommit, bw.locatie, bw.filename, bw.difftext, ci.author_id, pr.naam, " \
            "ci.commitdatumtijd from " + schema + ".bestandswijziging as bw " \
            "join " + schema + ".commitinfo as ci on bw.idcommit = ci.id " \
            "join " + schema + ".project as pr on ci.idproject = pr.id " \
            "where difftext is not null and extensie <> '.md' and bw.id >= {0} order by bw.id " \
            "limit({1});".format(result, limit)
        cursor = pg_db.execute_sql(sql)
        counter = 1
        for (bestandswijziging_id, id_commit, locatie, filename, diff_text, author_id, pr_name,
             commitdatumtijd) in cursor.fetchall():
            print("counter: " + str(counter))
            print("id: " + str(bestandswijziging_id))
            print("filename: " + filename)
            (new_lines, old_lines) = read_diff.read_diff_text(diff_text)
            if len(new_lines) > 0:
                print("new lines: " + str(len(new_lines)))
                print(new_lines)
                for (lijnnummer, tekst, primitives) in new_lines:
                    save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                                 list_to_string(primitives), 1, author_id, pr_name, commitdatumtijd)
            else:
                print("new lines: 0")
            if len(old_lines) > 0:
                print("old lines: " + str(len(old_lines)))
                print(old_lines)
                for (lijnnummer, tekst, primitives) in old_lines:
                    save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                                 list_to_string(primitives), -1, author_id, pr_name, commitdatumtijd)
            else:
                print("old lines: 0")
            print("--------------------")
            counter += 1

        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
