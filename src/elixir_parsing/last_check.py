import logging
import os
from collections import deque
from datetime import datetime

from peewee import *

from src.utils import configurator
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))
params_for_db = configurator.get_database_configuration()
schema = get_database_configuration().get('schema')
connection = None

terminals = ['identifier', 'kw_identifier', 'kw_identifier_safe', 'kw_identifier_unsafe', 'bracket_identifier',
             'paren_identifier', 'do_identifier', 'block_identifier', 'op_identifier', 'fn', 'end', 'alias', 'atom',
             'atom_quoted', 'atom_safe', 'atom_unsafe', 'bin_string', 'list_string', 'sigil', 'bin_heredoc',
             'list_heredoc', 'comp_op', 'at_op', 'unary_op', 'and_op', 'or_op', 'arrow_op', 'match_op', 'in_op',
             'in_match_op', 'type_op', 'dual_op', 'mult_op', 'power_op', 'concat_op', 'range_op', 'xor_op', 'pipe_op',
             'stab_op', 'when_op', 'capture_int', 'capture_op', 'assoc_op', 'rel_op', 'ternary_op', 'dot_call_op',
             'true', 'false', 'nil', 'do', 'eol', '";"', '","', '"."', '"("', '")"', '"["', '"]"', '"{"', '"}"', '"<<"',
             '">>"', '%{}', '%', 'int', 'flt', 'char', '.']

bestands_wijziging_sql = """
     select bw.id, a.tekstvooraf_tokens, a.tekstachteraf_tokens from {sch}.bestandswijziging bw
         join {sch}.commitinfo ci on bw.idcommit = ci.id
         join {sch}.abstract_syntax_trees a on bw.id = a.bestandswijziging_id
         join {sch}.bestandswijziging_zoekterm zt on bw.id = zt.idbestandswijziging
         where ci.idproject = {project_id} and zt.falsepositive = false
         group by bw.id, a.tekstvooraf_tokens, a.tekstachteraf_tokens, bw.tekstvooraf, bw.tekstachteraf, zt.idbestandswijziging  order by bw.id asc;
    """


def initialize():
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        encoding='utf-8')


def analyze_by_project(projectname, project_id):
    print(f"{Fore.BLUE}processing:" + projectname)
    print(f"{Fore.BLUE}project_id:" + str(project_id))
    bestandswijziging_cursor = get_connection().execute_sql(
        bestands_wijziging_sql.format(sch=schema, project_id=project_id))
    z = bestandswijziging_cursor.fetchall()
    for (bw_id, tekstvooraf_tokens, tekstachteraf_tokens) in z:  # per bestandswijziging
        zoekterm_regelnummers_new, zoekterm_regelnummers_old = get_bestandswijziging_zoekterm_regelnummer(bw_id)
        print(f"{Fore.BLUE}bestandswijziging_id: " + str(bw_id))
        if tekstvooraf_tokens is not None:
            # print("tekstvooraf_tokens")
            # print(tekstvooraf_tokens)
            parsed_lexeme_list = parsed_to_lexeme_list(tekstvooraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_old)
        if tekstachteraf_tokens is not None:
            # print("tekstachteraf_tokens")
            # print(tekstachteraf_tokens)
            parsed_lexeme_list = parsed_to_lexeme_list(tekstachteraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_new)


def get_data_withline_numbers(parsed_to_lexeme_list, zoektermenlijst):
    for bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort in zoektermenlijst:
        zoekterm_oke = False
        if zoekterm[0].isupper():
            filtered_list = list(filter(lambda x: x[0] == regelnummer and x[1] == ":alias" and x[2] == ":" + zoekterm,
                                        parsed_to_lexeme_list))
        else:
            filtered_list = list(filter(
                lambda x: x[0] == regelnummer and
                (x[1] in [":paren_identifier", ":do_identifier", ":identifier"]) and
                x[2] == ":" + zoekterm, parsed_to_lexeme_list))

        if len(filtered_list) > 0:
            zoekterm_oke = True

        if zoekterm_oke:
            print(f"{Fore.GREEN}zoekterm gevonden:" + zoekterm + ", regelnummer:" + str(regelnummer) + ", regelsoort:" + regelsoort)
            update_bestandswijziging_zoekterm_regelnummer(bzr_id, True)
        else:
            print(f"{Fore.RED}" + str(parsed_to_lexeme_list))
            print(f"{Fore.RED}niet gevonden: " + zoekterm + ", regelnummer:" + str(regelnummer) + ", regelsoort:" + regelsoort)
            update_bestandswijziging_zoekterm_regelnummer(bzr_id, False)


def update_bestandswijziging_zoekterm_regelnummer(bzr_id, is_valid):
    update_zoekterm_regelnummer_sql = """
    update {sch}.bestandswijziging_zoekterm_regelnummer set is_valid = {is_valid}  where id = {id}
    """.format(sch=schema, id=bzr_id, is_valid=is_valid)
    get_connection().execute_sql(update_zoekterm_regelnummer_sql)

def get_bestandswijziging_zoekterm_regelnummer(idbestandswijziging):
    selecteer_zoekterm_regelnummers = """
    select id, idbestandswijziging, zoekterm, regelnummer, regelsoort from 
    {sch}.bestandswijziging_zoekterm_regelnummer bzr where idbestandswijziging = {id}
    """.format(sch=schema, id=idbestandswijziging)
    regelnummers_cursor = get_connection().execute_sql(selecteer_zoekterm_regelnummers)
    zoekterm_regelnummers_new, zoekterm_regelnummers_old = [], []
    for (bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort) in regelnummers_cursor.fetchall():
        if regelsoort == 'nieuw':
            zoekterm_regelnummers_new.append((bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort))
        else:
            zoekterm_regelnummers_old.append((bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort))
    return zoekterm_regelnummers_new, zoekterm_regelnummers_old


def get_connection():
    global connection
    if connection is None:
        connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'),
                                        password=params_for_db.get('password'), host='localhost',
                                        port=params_for_db.get('port'))
    return connection


def parsed_to_lexeme_list(elixir_tokens):
    lexemes_list = []
    chars = deque(elixir_tokens)
    chars.popleft()  # remove first [
    chars.pop()  # remove last ]
    number_open_curly_braces = 0
    temp_part = ''
    new_part_start = False
    open_quote = False
    escaped = False
    while chars:
        char = read_next(chars)
        temp_part += char
        if not open_quote and char == '"':
            open_quote = True
        elif open_quote and char == '\\':
            escaped = True
        elif open_quote and escaped and char != '"':
            escaped = False
        elif open_quote and not escaped and char == '"':
            open_quote = False
        elif escaped and char == '"':
            escaped = False

        if not open_quote and char == '{':
            new_part_start = True
            number_open_curly_braces += 1
        elif not open_quote and char == '}':
            number_open_curly_braces -= 1
        if number_open_curly_braces == 0:
            if new_part_start:
                # print(temp_part)
                if '["\\"1\\""]}, {:"' in temp_part:
                    print("test")
                xxx = split_lexeme(temp_part)
                # print(xxx)
                lexemes_list.append(xxx)
            new_part_start = False
            temp_part = ''
    return lexemes_list


# {:identifier, {1, 1, ~c"defmodule"}, :defmodule}
# {:., {1, 16, nil}}

def split_lexeme(lexeme):
    if lexeme[0:2] != '{:':
        return -1, [], ''
    chars = deque(lexeme)
    chars.popleft()  # remove first [
    chars.pop()  # remove last ]
    first_part = None
    second_part = None
    temp_part = ''
    open_quote = False
    escaped = False
    while chars:
        char = read_next(chars)
        temp_part += char
        if not open_quote and char == '"':
            open_quote = True
        elif open_quote and char == '\\':
            escaped = True
        elif open_quote and escaped and char != '"':
            escaped = False
        elif open_quote and not escaped and char == '"':
            open_quote = False
        elif escaped and char == '"':
            escaped = False
        if not open_quote and char == ' ':
            continue
        if not open_quote and char == ',':
            temp_part = temp_part[:-1]
            first_part = temp_part
            temp_for_check = first_part
            if temp_for_check[0] == ':':
                temp_for_check = temp_for_check[1:]
            if temp_for_check not in terminals:
                logging.error('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
                raise Exception('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
            break
    temp_part = ''
    open_quote = False
    escaped = False
    number_open_curly_braces = 0
    while chars:
        char = read_next(chars)
        if char == ' ':
            continue
        temp_part += char
        if not open_quote and char == '"':
            open_quote = True
        elif open_quote and char == '\\':
            escaped = True
        elif open_quote and escaped and char != '"':
            escaped = False
        elif open_quote and not escaped and char == '"':
            open_quote = False
        elif escaped and char == '"':
            escaped = False
        if not open_quote and char == '{':
            number_open_curly_braces += 1
        elif not open_quote and char == '}':
            number_open_curly_braces -= 1
        if number_open_curly_braces == 0:
            second_part = temp_part
            break
    try:
        z = second_part.split(',')[0].split('{')[1]
    except IndexError:
        print(f"{Fore.CYAN}index error")
        print(lexeme)
        print(second_part)
        return -1, first_part, 'no third part'
    line_number = int(z)
    while chars:
        char = read_next(chars)
        if char == ' ':
            continue
        if char == ',':
            break
    temp_part = ''
    while chars:
        char = read_next(chars)
        temp_part += char
    the_rest = temp_part.strip()

    if first_part == ":bin_heredoc":
        print(f"{Fore.YELLOW}is bin_heredoc")
        print(the_rest)

    if first_part == ":sigil":
        print(f"{Fore.MAGENTA}a sigil")
        print(the_rest)

    return line_number, first_part, the_rest


def read_next(line_list):
    return line_list.popleft() if line_list else None


def analyze(process_identifier):
    oude_processtap = ' '
    nieuwe_processtap = 'last_check'

    try:
        db_postgresql.open_connection()
        db_postgresql.registreer_processor(process_identifier)
        volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
        rowcount = volgend_project[2]
        while rowcount == 1:
            projectnaam = volgend_project[1]
            projectid = volgend_project[0]
            verwerking_status = 'mislukt'

            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                analyze_by_project(projectnaam, projectid)
                verwerking_status = 'verwerkt'
            # continue processing next project
            except Exception as e_inner:
                logging.error('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
                logging.exception(e_inner)

            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid)
            volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
            rowcount = volgend_project[2]

        # na de loop
        db_postgresql.deregistreer_processor(process_identifier)
    except Exception as e_outer:
        logging.error('Er zijn fouten geconstateerd tijdens het loopen door de projectenlijst. Zie details hieronder')
        logging.exception(e_outer)


if __name__ == '__main__':
    print(datetime.now())
    analyze_by_project('nickjj/docker-web-framework-examples', 2438)
    print(datetime.now())
