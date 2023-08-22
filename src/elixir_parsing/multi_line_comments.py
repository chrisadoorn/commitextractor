import logging
import os
from datetime import datetime
from peewee import *

from src.utils import configurator
from src.utils.configurator import get_database_configuration

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))
params_for_db = configurator.get_database_configuration()
schema = get_database_configuration().get('schema')


def initialize():
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        encoding='utf-8')


def check_op_multiline_comments():
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    bestands_wijziging_sql_dist = "select distinct idbestandswijziging from {sch}.bestandswijziging_zoekterm bw_zt " \
                                  "where bw_zt.falsepositive = false order by bw_zt.idbestandswijziging asc;".format(
        sch=schema)

    selecteer_teksten_sql = "select tekstvooraf, tekstachteraf from {sch}.bestandswijziging bw where id = {id};"

    selecteer_zoekterm_regelnummers = "select id, idbestandswijziging, zoekterm, regelnummer, regelsoort from {sch}.bestandswijziging_zoekterm_regelnummer bzr where idbestandswijziging = {id};"

    bestandswijziging_zoekterm_cursor = connection.execute_sql(bestands_wijziging_sql_dist)

    for (idbestandswijziging,) in bestandswijziging_zoekterm_cursor.fetchall():  # per bestandswijziging
        ml_comments = []
        bestandswijziging_cursor = connection.execute_sql(
            selecteer_teksten_sql.format(sch=schema, id=idbestandswijziging))
        (tekstvooraf, tekstachteraf) = bestandswijziging_cursor.fetchone()  # haal de tekst voor en na de wijziging op
        ml_comments_min = findMultiLineComments(tekstvooraf)  # lijst met multi-line comments voor de wijziging
        ml_comments_plus = findMultiLineComments(tekstachteraf)  # lijst met multi-line comments na de wijziging
        regelnummers_cursor = connection.execute_sql(
            selecteer_zoekterm_regelnummers.format(sch=schema, id=idbestandswijziging))
        for (id, idbestandswijziging, zoekterm, regelnummer,
             regelsoort) in regelnummers_cursor.fetchall():  # zoektermen met regelnummers
            r = (id, idbestandswijziging, zoekterm, regelnummer, regelsoort)
            if regelsoort == 'oud':
                for (start, end) in ml_comments_min:
                    if start <= regelnummer <= end:
                        print('regel {0} is een multi-line comment'.format(regelnummer))
                        ml_comments = ml_comments + [r]
                        break  # regelnummer valt af
            elif regelsoort == 'nieuw':
                for (start, end) in ml_comments_plus:
                    if start <= regelnummer <= end:
                        print('regel {0} is een multi-line comment'.format(regelnummer))
                        ml_comments = ml_comments + [r]
                        break  # regelnummer valt af

        for (id, idbestandswijziging, zoekterm, regelnummer, regelsoort) in ml_comments:
            if regelsoort == 'oud':
                substract_sql_min = "UPDATE {sch}.bestandswijziging_zoekterm set aantalgevonden_oud = aantalgevonden_oud -1 " \
                                    "WHERE idbestandswijziging={idbestandswijziging} and zoekterm='{zoekterm}' ".format(
                    sch=schema, idbestandswijziging=idbestandswijziging, zoekterm=zoekterm)
                connection.execute_sql(substract_sql_min)
            elif regelsoort == 'nieuw':
                substract_sql_plus = "UPDATE {sch}.bestandswijziging_zoekterm set aantalgevonden_nieuw = aantalgevonden_nieuw -1 " \
                                     "WHERE idbestandswijziging={idbestandswijziging} and zoekterm='{zoekterm}' ".format(
                    sch=schema, idbestandswijziging=idbestandswijziging, zoekterm=zoekterm)
                connection.execute_sql(substract_sql_plus)
            delete_sql = "DELETE FROM {sch}.bestandswijziging_zoekterm_regelnummer " \
                         "WHERE idbestandswijziging={idbestandswijziging} and regelnummer={regelnummer} " \
                         "and regelsoort='{regelsoort}' ".format(sch=schema, idbestandswijziging=idbestandswijziging,
                                                                 regelnummer=regelnummer, regelsoort=regelsoort)
            connection.execute_sql(delete_sql)




def findMultiLineComments(tekst):
    # in elixir is dit niet mogelijk:
    # """ comment """
    # of  """ comment
    # of
    # comment """
    # tekst
    # """  expression
    # alleen dit"
    # a = """      \\de tekst voor """ is al beoordeeld
    # comment
    # bla bla
    # """ evt code    \\ e tekst na """ is al beoordeeld
    # Deze methode vindt teksten te die tussen """ en """ liggen
    if tekst is None:
        return []
    regels = tekst.split('\n')
    r = 0
    start_gevonden = False
    start_regel = -1
    lijst = []
    for regel in regels:
        r = r + 1
        if start_gevonden is False and regel.find('"""') >= 0:
            start_gevonden = True
            start_regel = r
            continue
        if start_gevonden is True and regel.find('"""') >= 0:
            start_gevonden = False
            stop_regel = r
            lijst = lijst + [(start_regel, stop_regel)]
    return lijst


def printMetRegels(tekst):
    regels = tekst.split('\n')
    r = 1
    for regel in regels:
        print(str(r) + ":" + regel)
        r = r + 1


if __name__ == '__main__':
    check_op_multiline_comments()
