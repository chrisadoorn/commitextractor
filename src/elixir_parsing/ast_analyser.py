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


def retrieveAsts():
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    bestandswijziging_sql = """
    select distinct ast.bestandswijziging_id, ast.tekstvooraf_ast, ast.tekstachteraf_ast
    from {sch}.abstract_syntax_trees ast
    join {sch}.bestandswijziging_zoekterm bwz on ast.bestandswijziging_id = bwz.idbestandswijziging
    where bwz.aantalgevonden_oud > 0 or bwz.aantalgevonden_nieuw > 0 order by ast.bestandswijziging_id
    limit 1000;
    """.format(sch=schema)

    bestandswijziging_ast_cursor = connection.execute_sql(bestandswijziging_sql)
    for (bestandswijziging_id, tekstvooraf_ast, tekstachteraf_ast) in bestandswijziging_ast_cursor.fetchall():
        print(bestandswijziging_id)

        voor =  analyse_ast(tekstvooraf_ast)

        na = analyse_ast(tekstachteraf_ast)

        bestandswijziging_zt_rn_sql = \
            """
            select bwzrn.regelnummer, bwzrn.zoekterm, bwzrn.regelsoort
            from {sch}.bestandswijziging_zoekterm_regelnummer bwzrn
            where bwzrn.idbestandswijziging = {idbwz};
            """ \
            .format(sch=schema, idbwz=bestandswijziging_id)

        bestandswijziging_zt_rn_cursor = connection.execute_sql(bestandswijziging_zt_rn_sql)
        list_of_line_numbers = []
        for (regelnummer, zoekterm, regelsoort) in bestandswijziging_zt_rn_cursor.fetchall():
            list_of_line_numbers.append(regelnummer)
            print(regelnummer, zoekterm, regelsoort)

        for (a, b) in voor:
            if b in list_of_line_numbers:
                print(a + " " + str(b) + ", lnr in gevonden regels")

        for (a, b) in na:
            if b in list_of_line_numbers:
                print(a + " " + str(b) + ", lnr in gevonden regels")


def analyse_ast(text_containing_ast):
    first_terms = []
    if text_containing_ast is None:
        return first_terms
    lines = text_containing_ast.splitlines()
    for line in lines:
        line_list = deque(line)
        if line_list[0] == '{':
            print(line)
            xxx = read_first_term(line_list)
            first_terms.extend(xxx)
        else:
            print("geen ast")

    return first_terms


def read_first_term(line_list):
    first_terms = []
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
                if term == ':.':
                    x = getkwalified_parts(line_list)
                    print(x)
            term = ''
        elif term != '':
            term += char
    return first_terms


def read_second_term(line_list): # linenummbers
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
        if char == '{':   # start of tuple
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


if __name__ == '__main__':
    retrieveAsts()