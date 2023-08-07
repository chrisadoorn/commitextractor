import os
from collections import deque
from datetime import datetime
from peewee import *

from src.utils import configurator
from src.utils.configurator import get_database_configuration

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))
params_for_db = configurator.get_database_configuration()
schema = get_database_configuration().get('schema')

"""
Check module usage:
Agent
GenServer
Node
Process
Supervisor
Task
Registry
DynamicSupervisor

Deze zijn altijd van de vorm Term.xxx
Het gaat er om dit soort gevallen te vinden, dus onafhankelijk van wat achter de punt staat.

Dit is de vorm in de ast :

{:., [line: 6], [{:__aliases__, [line: 6], [:GenServer]}, :call]}

:. de dot operator,
[line: 6] het regelnummer

[{:__aliases__, [line: 6], [:GenServer]}, :call] de linker en rechter term van de dot operator
{:__aliases__, [line: 6], [:GenServer]} de linker term van de dot operator
:call de rechter term van de dot operator
:__aliases__ geeft aan dat het om eem module gaat
:GenServer de naam van de module
:call de naam van de functie

Stategie: vindt deze sub AST's,
:. dot operator
Vind linker en rechter term
Controleer of linker helft icm regelnummer in de bestandswijzigingen. 


{:., [line: 6], [{:__aliases__, [line: 6], [:GenServer]}, :call]}



No valid match:
    opts = [strategy: :one_for_one, name: SyncM.Supervisor]

"""


def retrieveAsts():
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    bestandswijziging_sql = """
    select distinct ast.bestandswijziging_id, bw.tekstvooraf, bw.tekstachteraf, ast.tekstvooraf_ast, ast.tekstachteraf_ast
    from {sch}.abstract_syntax_trees ast
    join {sch}.bestandswijziging_zoekterm bwz on ast.bestandswijziging_id = bwz.idbestandswijziging
    join {sch}.bestandswijziging bw on ast.bestandswijziging_id = bw.id
    where (bwz.aantalgevonden_oud > 0 or bwz.aantalgevonden_nieuw > 0)  order by ast.bestandswijziging_id
    limit 1000;
    """.format(sch=schema)

    bestandswijziging_ast_cursor = connection.execute_sql(bestandswijziging_sql)
    for (bestandswijziging_id, tekstvooraf, tekstachteraf, tekstvooraf_ast,
         tekstachteraf_ast) in bestandswijziging_ast_cursor.fetchall():
        print(bestandswijziging_id)
        bestandswijziging_zt_rn_sql = """
            select bwzrn.regelnummer, bwzrn.zoekterm, bwzrn.regelsoort
            from {sch}.bestandswijziging_zoekterm_regelnummer bwzrn
            where bwzrn.idbestandswijziging = {idbwz};
            """.format(sch=schema, idbwz=bestandswijziging_id)

        bestandswijziging_zt_rn_cursor = connection.execute_sql(bestandswijziging_zt_rn_sql)
        list_of_line_numbers = []
        for (regelnummer, zoekterm, regelsoort) in bestandswijziging_zt_rn_cursor.fetchall():
            list_of_line_numbers.append(regelnummer)
            print(regelnummer, zoekterm, regelsoort)

        print("__vooraf__")
        voor= analyse_ast(tekstvooraf_ast)
        print("__achteraf__")
        na= analyse_ast(tekstachteraf_ast)

   #    for (a, b) in yy:
   #        print(" left part: " + str(a))
   #        print(" right part: " + str(b))
   #        insert_sql = """
   #        insert into {sch}.keywords_found_in_asts (bestandswijziging_id, line_number, lefthand_side, righthand_side, primitive_call)
   #            values (
   #            {bestandswijziging_id} ,
   #            {line_number} ,
   #            {left_hand_side},
   #            {righthand_side},
   #            '{primitive_call}'
   #            )
   #        """.format(sch=schema, bestandswijziging_id=bestandswijziging_id, line_number=0
   #                   , left_hand_side=__opkuizen_speciale_tekens(a), righthand_side=__opkuizen_speciale_tekens(b),
   #                   primitive_call='')
   #        #  connection.execute_sql(insert_sql)


   # https://github.com/elixir-lang/elixir/blob/main/lib/elixir/src/elixir_parser.yrl
def analyse_ast(text_containing_ast):
    first_terms = []
    if text_containing_ast is None:
        return [],[]
    lines = text_containing_ast.splitlines()
    for line in lines:
        line_list = deque(line)
        if line_list[0] == '{':  # ast nust start with '{'
            print(line)
            find_type_of_action(line_list)
            # xxx = read_first_terms_of_AST_tuple(line_list)
            # first_terms.extend(xxx)
        else:
            print("geen ast")
            return [],[]

    return first_terms


def find_type_of_action(line_list):
    while line_list:
        char = read_next(line_list)
        if char is None:
            break
        if char == ' ':  # skip whitespace
            continue
        if char == '{':  # end of first term
            char = read_next(line_list)
            if char is None:
                break
            if char == ':':
                a,b,c = read_action(line_list)
                if a != 'other':
                    print(a,b,c)
            else:
                put_back(line_list, char)

def read_next(line_list):
     return line_list.popleft() if line_list else None


def put_back(line_list, ch):
    line_list.appendleft(ch)


def read_action(line_list):
    collected = ''
    read = True
    while read:
        char = read_next(line_list)
        if char is None or char == ',':
            read = False
            continue
        collected += char
    if collected in ['use', '.', 'spawn', 'spawn_link', 'spawn_monitor', 'send', 'receive']:
        n, t = read_use(line_list)
        return collected, n, t
    else:
        return 'other', 0, ''


def read_use(line_list):
    read = True
    word_to_find = 'line:'
    collected = ''
    line_number = -1
    # read line number
    while read:
        char = read_next(line_list)
        if char is None:
            read = False
            break
        if char == ' ':  # skip whitespace
            continue
        if line_number < 0 and char == '[':  # start meta from_brackets , no_parens
            read_line_number = True
            get_number = False
            while read_line_number:
                char = read_next(line_list)
                if char is None:
                    read_line_number = False
                    read = False
                    break
                if char == ']':  # skip whitespace
                    read_line_number = False
                    continue
                collected += char
                if not get_number and collected == word_to_find:
                    get_number = True
                    collected = ''
                    continue
                if not get_number and word_to_find.find(collected) != 0:
                    collected = ''

            line_number = int(collected)
        # past line number
        if line_number > 0 and char == '[':
            read = False
            put_back(line_list, char)

    text = read_aliasses(line_list)
    return line_number, text


def read_aliasses(line_list):
    read = True
    text = ''
    brackets = deque('')
    while read:
        char = read_next(line_list)
        if char is None:
            break
        if char == '[' or char == '{':
            brackets.append(char)
        if char == ']' or char == '}':
            brackets.pop()
        text += char
        if not brackets:
            read = False
    return text


def read_first_terms_of_AST_tuple(line_list)  :   # each nested tuple start with '{:', the term after that until the first ',' are collected
    first_terms = []
    qualified_parts = []
    term = ''
    while line_list:
        char = line_list.popleft()
        if term == '' and char == ' ':  # skip whitespace
            continue
        if char == '{':  # end of first term
            prev_char = char
            char = line_list.popleft() if line_list else ''
            if char == ':':
                term += char
                continue
            else:
                line_list.appendleft(char)
                char = prev_char
        if term != '' and char == ',':
            line_number = read_second_term(line_list)
            if line_number > 0:
                first_terms.append((term, line_number))
                if term == ':.':  # is the dot
                    x = getkwalified_parts(line_list)
                    qualified_parts.append(x)
                    # print(x)
            term = ''
        elif term != '':
            term += char
    return first_terms, qualified_parts


def read_second_term(line_list):  # linenummbers
        term = ''
        while line_list:
            char = line_list.popleft() if line_list else ''
            if char == '':
                break
            if term == '' and char == ' ':  # skip whitespace
                continue
            if term != '' and char == ',':  # end of first term
                break
            else:
               term += char

        return get_line_number(term)


def get_line_number(term):
    if term == '[]':
        return 0
    term = term.replace('[line:', '')
    term = term.replace(']', '')
    try:
        return int(term)
    except ValueError:
        return -9


def getkwalified_parts(line_list):
    term = ''
    left_part = ''
    right_part = ''
    while line_list:
        char = line_list.popleft() if line_list else ''
        if char == '':
            return left_part, right_part
        if term == '' and char == ' ':  # skip whitespace
            continue
        if char == '[':
            return (get_one_hand_side(line_list, 'left'),
                    get_one_hand_side(line_list, 'right'))

    return left_part, right_part


def get_one_hand_side(line_list, left_or_right = 'left'):
    term = ''
    brackets = deque('')
    while line_list:  # lees tussen [ en ]
        char = line_list.popleft() if line_list else ''
        if char == '':
            return term
        if term == '' and char == ' ':  # skip whitespace
            continue
        if char ==  '{':   # start of tuple
            brackets.append(char)
        if char == '}':
            if brackets:
                brackets.pop()
        if left_or_right == 'left' and char == ',' and not brackets:
            return term
        if left_or_right == 'right' and char == ']' and not brackets:
            return term
        else:
            term += char


# types of mc usage:
# direct call of primitive
# use of behaviour
# call a


# Ast literals
# atoms  :atom
# integers  123
# floats  12.3
# lists  [1,2,3]
# strings  "hello"
# 2 element tuples containing above {1.23 :atom}


def __opkuizen_speciale_tekens(tekst,not_null = False):
    """
    Speciale tekens toevoegen aan een string voor gebruik in een PSQL statement
    """
    if tekst is None:
        if not_null:
            return "''"
        return 'null'
    try:
        tekst = tekst.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    return "'" + tekst.replace("'", "''").replace("%", "%%") + "'"




if __name__ == '__main__':
    retrieveAsts()
