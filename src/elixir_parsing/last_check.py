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
    # haal tekstvooraf_tokens en tekstachteraf_tokens per bestandswijziging / voor een project
    # doorloop deze lijst
    for (bw_id, tekstvooraf_tokens, tekstachteraf_tokens) in z:  # per bestandswijziging
        zoekterm_regelnummers_new, zoekterm_regelnummers_old = get_bestandswijziging_zoekterm_regelnummer(bw_id)
        print(f"{Fore.BLUE}bestandswijziging_id: " + str(bw_id))
        if tekstvooraf_tokens is not None:
            parsed_lexeme_list = parsed_to_lexeme_list(tekstvooraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_old)
        if tekstachteraf_tokens is not None:
            parsed_lexeme_list = parsed_to_lexeme_list(tekstachteraf_tokens)
            get_data_withline_numbers(parsed_lexeme_list, zoekterm_regelnummers_new)


def get_data_withline_numbers(parsed_to_lexeme_list, zoektermenlijst):
    for bzr_id, idbestandswijziging, zoekterm, regelnummer, regelsoort in zoektermenlijst:
        zoekterm_oke = False
        if zoekterm[0].isupper():  # if first letter is uppercase, then it is a module name
            filtered_list = list(filter(lambda x: x[0] == regelnummer and x[1] == ":alias" and x[2] == ":" + zoekterm,
                                        parsed_to_lexeme_list))
        else:  # if first letter not uppercase, then it is a function name
            filtered_list = list(filter(
                lambda x: x[0] == regelnummer and (x[1] in [":paren_identifier", ":do_identifier", ":identifier"]) and
                          x[2] == ":" + zoekterm, parsed_to_lexeme_list))

        if len(filtered_list) > 0:
            zoekterm_oke = True

        if zoekterm_oke:
            print(f"{Fore.GREEN}zoekterm gevonden:" + zoekterm + ", regelnummer:" + str(
                regelnummer) + ", regelsoort:" + regelsoort)
            update_bestandswijziging_zoekterm_regelnummer(bzr_id, True)
        else:
            print(f"{Fore.RED}" + str(parsed_to_lexeme_list))
            print(f"{Fore.RED}niet gevonden: " + zoekterm + ", regelnummer:" + str(
                regelnummer) + ", regelsoort:" + regelsoort)
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


def parsed_to_lexeme_list(elixir_tokens) -> list[tuple[int, str, str]]:
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
                xxx = split_lexeme(temp_part)
                # print(xxx)
                lexemes_list.append(xxx)
            new_part_start = False
            temp_part = ''
    return lexemes_list


def split_lexeme(token_string) -> tuple[int, str, str]:
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
        return -1, '', ''
    chars = deque(token_string)
    chars.popleft()  # remove first {
    chars.pop()  # remove last }
    first_part = get_first_part(chars)
    line_number = get_second_part(chars)
    if line_number < 0:
        return -1, first_part, 'no third part'
    the_rest = get_third_part(chars)
    return line_number, first_part, the_rest


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
            if temp_for_check not in terminals:
                logging.error('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
                raise Exception('First part is no a terminal. {lexeme}  '.format(lexeme=temp_for_check))
            break
    return first_part


def get_second_part(chars):
    temp_part = ''
    open_quote = False
    escaped = False
    number_open_curly_braces = 0
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
        z = second_part.split(',')[0].split('{')[1]
        return int(z)
    except IndexError:
        print(f"{Fore.CYAN}index error")
        return -1


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
