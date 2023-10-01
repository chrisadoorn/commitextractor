import logging
import os
from collections import deque
from datetime import datetime

from colorama import Fore
from colorama import init as colorama_init
from peewee import *

from src.utils import configurator
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration

SELECT_BESTANDSWIJZIGING_ZOEKTERM_REGELNUMMER = """
select id, idbestandswijziging, zoekterm, regelnummer, regelsoort from 
{sch}.bestandswijziging_zoekterm_regelnummer bzr where idbestandswijziging = {id}
"""

UPDATE_BESTANDSWIJZIGING_ZOEKTERM_REGELNUMMER = """
update {sch}.bestandswijziging_zoekterm_regelnummer set is_valid_3 = {is_valid}  where id = {id}
"""

colorama_init()

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))
params_for_db = configurator.get_database_configuration()
schema = get_database_configuration().get('schema')
connection = None


TERMINALS = ['identifier', 'kw_identifier', 'kw_identifier_safe', 'kw_identifier_unsafe', 'bracket_identifier',
             'paren_identifier', 'do_identifier', 'block_identifier', 'op_identifier', 'fn', 'end', 'alias', 'atom',
             'atom_quoted', 'atom_safe', 'atom_unsafe', 'bin_string', 'list_string', 'sigil', 'bin_heredoc',
             'list_heredoc', 'comp_op', 'at_op', 'unary_op', 'and_op', 'or_op', 'arrow_op', 'match_op', 'in_op',
             'in_match_op', 'type_op', 'dual_op', 'mult_op', 'power_op', 'concat_op', 'range_op', 'xor_op', 'pipe_op',
             'stab_op', 'when_op', 'capture_int', 'capture_op', 'assoc_op', 'rel_op', 'ternary_op', 'dot_call_op',
             'true', 'false', 'nil', 'do', 'eol', '";"', '","', '.', '"("', '")"', '"["', '"]"', '"{"', '"}"', '"<<"',
             '">>"', '%{}', '%', 'int', 'flt', 'char']


TERMINALS_LIST_SPECIFICATION = [(':identifier', 3, 'un-nested'), (':kw_identifier', 3, 'un-nested'),
    (':kw_identifier_unsafe', 3, 'nested'), (':bracket_identifier', 2, 'un-nested'),
    (':paren_identifier', 3, 'un-nested'), (':do_identifier', 3, 'un-nested'), (':block_identifier', 3, 'un-nested'),
    (':op_identifier', 3, 'un-nested'), (':fn', 2, 'un-nested'), (':end', 2, 'un-nested'), (':alias', 3, 'un-nested'),
    (':atom', 2, 'un-nested'), (':atom_quoted', 3, 'un-nested'), (':atom_unsafe', 3, 'nested'),
    (':bin_string', 3, 'un-nested'), (':list_string', 3, 'un-nested'), (':sigil', 7, 'un-nested'),
    (':bin_heredoc', 4, 'un-nested'), (':list_heredoc', 4, 'un-nested'), (':comp_op', 3, 'un-nested'),
    (':at_op', 3, 'un-nested'), (':unary_op', 3, 'un-nested'), (':and_op', 3, 'un-nested'), (':or_op', 3, 'un-nested'),
    (':arrow_op', 3, 'un-nested'), (':match_op', 3, 'un-nested'), (':in_op', 3, 'un-nested'),
    (':in_match_op', 3, 'un-nested'), (':type_op', 3, 'un-nested'), (':dual_op', 3, 'un-nested'),
    (':mult_op', 3, 'un-nested'), (':power_op', 3, 'un-nested'), (':concat_op', 3, 'un-nested'),
    (':range_op', 3, 'un-nested'), (':xor_op', 3, 'un-nested'), (':pipe_op', 3, 'un-nested'),
    (':stab_op', 3, 'un-nested'), (':when_op', 3, 'un-nested'), (':capture_int', 3, 'un-nested'),
    (':capture_op', 3, 'un-nested'), (':assoc_op', 3, 'un-nested'), (':rel_op', 3, 'un-nested'),
    (':ternary_op', 3, 'un-nested'), (':dot_call_op', 3, 'un-nested'), ('true', 2, 'un-nested'),
    ('false', 2, 'un-nested'), (':do', 2, 'un-nested'), (':eol', 2, 'un-nested'), (':";"', 2, 'un-nested'),
    (':","', 2, 'un-nested'), (':.', 2, 'un-nested'), (':"("', 2, 'un-nested'), (':")"', 2, 'un-nested'),
    (':"["', 2, 'un-nested'), (':"]"', 2, 'un-nested'), (':"{"', 2, 'un-nested'), (':"}"', 2, 'un-nested'),
    (':"<<"', 2, 'un-nested'), (':">>"', 2, 'un-nested'), (':%{}', 2, 'un-nested'), (':%', 2, 'un-nested'),
    (':int', 3, 'un-nested'), (':flt', 3, 'un-nested'), (':char', 3, 'un-nested')]


BESTANDS_WIJZIGING_SQL = """
select bw.id, a.tekstvooraf_tokens, a.tekstachteraf_tokens from {sch}.bestandswijziging bw
     join {sch}.commitinfo ci on bw.idcommit = ci.id
     join {sch}.abstract_syntax_trees a on bw.id = a.bestandswijziging_id
     join {sch}.bestandswijziging_zoekterm zt on bw.id = zt.idbestandswijziging
     where ci.idproject = {project_id}
     group by bw.id, a.tekstvooraf_tokens, a.tekstachteraf_tokens, bw.tekstvooraf, bw.tekstachteraf, zt.idbestandswijziging  order by bw.id asc;
"""


def initialize():
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        encoding='utf-8')


def analyze_by_project(projectname, project_id):
    print(f"{Fore.BLUE}processing:" + projectname)
    print(f"{Fore.BLUE}project_id:" + str(project_id))
    bestandswijziging_cursor = get_connection().execute_sql(
        BESTANDS_WIJZIGING_SQL.format(sch=schema, project_id=project_id))
    z = bestandswijziging_cursor.fetchall()
    for (bw_id, tekstvooraf_tokens, tekstachteraf_tokens) in z:  # per bestandswijziging
        zoekterm_regelnummers_new, zoekterm_regelnummers_old = get_bestandswijziging_zoekterm_regelnummer(bw_id)
        print(f"{Fore.BLUE}bestandswijziging_id: " + str(bw_id))
        if tekstvooraf_tokens is not None:
            parsed_lexeme_list = parse_lexeme_list(tekstvooraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_old)
        if tekstachteraf_tokens is not None:
            parsed_lexeme_list = parse_lexeme_list(tekstachteraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_new)


def parse_lexeme_list(tekst_tokens):
    lexeme_list = parse_to_lexeme_list(tekst_tokens)
    parsed_lexeme_list = []
    counter = 0
    for le in lexeme_list:
        parsed_lexeme_list.append((counter, split_lexeme(le)))
        counter += 1
    return parsed_lexeme_list


def get_data_withline_numbers(parsed_to_lexeme_list, zoektermenlijst):
    """

    :param parsed_to_lexeme_list:  list[tuple[int, tuple[int, int, str, str]]
    :param zoektermenlijst:  list[tuple[int, int, str,int,str]]
    :return:
    """
    for bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort in zoektermenlijst:
        # if first letter is uppercase, then it is a module name
        if zoekterm[0].isupper():
            zoekterm_oke = zoekterm_oke_module_type(zoekterm, parsed_to_lexeme_list, regelnummer)
        else:  # if first letter not uppercase, then it is a function name
            zoekterm_oke = zoekterm_oke_function_type(zoekterm, parsed_to_lexeme_list, regelnummer)
        update_bestandswijziging_zoekterm_regelnummer(bzr_id, zoekterm_oke)


def zoekterm_oke_function_type(zoekterm, parsed_to_lexeme_list, regelnummer):
    zoekterm_oke = False
    filtered_list = list(filter(
        lambda x: x[1][0] == regelnummer and (x[1][2] in [":paren_identifier", ":do_identifier", ":identifier"]) and
                  x[1][3] == ":" + zoekterm, parsed_to_lexeme_list))
    for (list_nr, (_, _, _, _)) in filtered_list:
        if parsed_to_lexeme_list[list_nr - 1][1][3] == ":def" or parsed_to_lexeme_list[list_nr - 1][1][3] == ":defp":
            break
        if parsed_to_lexeme_list[list_nr - 2][1][3] == ":Kernel" and parsed_to_lexeme_list[list_nr - 1][1][
            2] == ":.":  # if the previous token is a dot, then it is a function name
            zoekterm_oke = True
            break
        elif parsed_to_lexeme_list[list_nr - 1][1][2] != ":.":
            zoekterm_oke = True
            break
    return zoekterm_oke


def zoekterm_oke_module_type(zoekterm, parsed_to_lexeme_list, regelnummer):
    filtered_list = list(filter(lambda x: x[1][0] == regelnummer and x[1][2] == ":alias" and x[1][3] == ":" + zoekterm,
                                parsed_to_lexeme_list))
    zoekterm_oke = False
    for (list_nr, (ln_nr, col_nr, type, term)) in filtered_list:  # could be more than 1 zoekterm on a line
        if parsed_to_lexeme_list[list_nr - 1][1][2] == ":.":  # if the previous token is a dot, then it is a function name
            continue
        elif parsed_to_lexeme_list[list_nr + 1][1][2] == ":.":
            zoekterm_oke = True
            break
        else:
            list_with_use = list(filter(
                lambda x: x[1][0] == regelnummer and x[1][1] < col_nr and x[1][2] == ":identifier" and x[1][
                    3] == ":use", parsed_to_lexeme_list))
            if len(list_with_use) > 0:
                zoekterm_oke = True
                break
    return zoekterm_oke


def update_bestandswijziging_zoekterm_regelnummer(bzr_id, is_valid):
    update_zoekterm_regelnummer_sql = UPDATE_BESTANDSWIJZIGING_ZOEKTERM_REGELNUMMER.format(sch=schema, id=bzr_id, is_valid=is_valid)
    get_connection().execute_sql(update_zoekterm_regelnummer_sql)


def get_bestandswijziging_zoekterm_regelnummer(idbestandswijziging):
    selecteer_zoekterm_regelnummers = (SELECT_BESTANDSWIJZIGING_ZOEKTERM_REGELNUMMER
                                       .format(sch=schema, id=idbestandswijziging))
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


def parse_to_lexeme_list(elixir_tokens) -> list[str]:
    """
    The input is a string containing a list of token_string.
    The first and last character of the string are [ and ].
    The string is split into a list of token_string.
    The string is read from left to right, a token string start with a {: and ends with a }.
    The token string list is divided by a comma's.
    The end of a token string is determined by the number of open curly braces, if this is 0,
    then the token string ends.
    All escaped curly braces inside a strings are ignored.
    Each token string splits into 3 parts:
    The identifier, the line number and the attribute value.
    :param elixir_tokens:
    :return: a list of tuples containing the line number, the identifier and the attribute value
    """
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
        open_quote, escaped = handle_quotes(char, escaped, open_quote)
        if not open_quote and char == '{':
            new_part_start = True
            number_open_curly_braces += 1
        elif not open_quote and char == '}':
            number_open_curly_braces -= 1
        if number_open_curly_braces == 0:
            if new_part_start:
                lexemes_list.append(temp_part)
            new_part_start = False
            temp_part = ''
    return lexemes_list


def split_lexeme(token_string) -> tuple[int, int, str, str]:
    """
    A token string is a string containing 3 parts.
    First part is the token name, this must be in the terminals list.
    Second contains meta info including the line number the token is on.
    Third part is the attribute value
    This:
    {:identifier, {1, 1, ~c"defmodule"}, :defmodule}
    means:
    The identifier defmodule is on line 1
    This:
    {:bin_string, {29, 7, nil}, ["{% assign a = b | divided_by: 4 %}"]}
    means:
    A string with the value "{% assign a = b | divided_by: 4 %}" is on line 29
    This function splits the token string into the 3 parts:
    The identifier, the line number and the attribute value.
    """
    if token_string[0:2] != '{:':  # must start with {:, otherwise it is not a token
        return  -1, -1, '', ''
    chars = deque(token_string)
    chars.popleft()  # remove first {
    chars.pop()  # remove last }
    first_part = get_first_part(chars)
    output = list(filter(lambda x: x[0] == first_part, TERMINALS_LIST_SPECIFICATION))[0]
    line_number = get_line_column_nrs(chars)
    if output[1] < 3:
        return line_number[0], line_number[1], first_part, ''
    the_rest = get_third_part(chars)
    return line_number[0], line_number[1], first_part, the_rest


def get_first_part(chars):
    open_quote = False
    escaped = False
    first_part = None
    temp_part = ''
    while chars:
        char = read_next(chars)
        temp_part += char
        open_quote, escaped = handle_quotes(char, escaped, open_quote)
        if not open_quote and char == ' ':
            continue
        if not open_quote and char == ',':
            temp_part = temp_part[:-1]
            first_part = temp_part
            temp_for_check = first_part
            if temp_for_check[0] == ':':
                temp_for_check = temp_for_check[1:]
            if temp_for_check not in TERMINALS:
                logging.error('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
                raise Exception('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
            break
    return first_part


def get_line_column_nrs(chars):
    temp_part = ''
    open_quote = False
    escaped = False
    number_open_curly_braces = 0
    second_part = ''
    while chars:
        char = read_next(chars)
        if char == ' ':
            continue
        temp_part += char
        open_quote, escaped = handle_quotes(char, escaped, open_quote)

        if not open_quote and char == '{':
            number_open_curly_braces += 1
        elif not open_quote and char == '}':
            number_open_curly_braces -= 1
        if number_open_curly_braces == 0:
            second_part = temp_part
            break
    try:
        line_nr = second_part.split(',')[0].split('{')[1]
        column_nr = second_part.split(',')[1].strip()
        return int(line_nr), int(column_nr)
    except IndexError:
        print(f"{Fore.CYAN}index error")
        return -1, -1


def handle_quotes(char, escaped, open_quote):
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
    return open_quote, escaped


def get_third_part(chars):
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
    return temp_part.strip()


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
