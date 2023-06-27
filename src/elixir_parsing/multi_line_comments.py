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

# todo: uitzonderingen, een keyword dat als parameter naam wordt gebruikt, multi-line comments """ en """


def verzamel_alle_primitieven_per_file():
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    sql1 = "select idbestandswijziging, zoekterm, regelnummers from {sch}.bestandswijziging_zoekterm bw_zt " \
          "where bw_zt.falsepositive = false order by idbestandswijziging;".format(sch=schema)

    sql2 = "select difftext, tekstachteraf from {sch}.bestandswijziging bw where id = {id};"

    cursor = connection.execute_sql(sql1)
    vorige_idbestandswijziging = -1
    for (idbestandswijziging, zoekterm, regelnummers ) in cursor.fetchall():
        if idbestandswijziging != vorige_idbestandswijziging:
            if vorige_idbestandswijziging > 0:
                input("Press Enter to continue...")
                print('einde bestandswijziging {0}'.format(vorige_idbestandswijziging))
            vorige_idbestandswijziging = idbestandswijziging
            print('begin bestandswijziging {0}'.format(idbestandswijziging))
            cursor2 = connection.execute_sql(sql2.format(sch=schema, id=idbestandswijziging))
            (difftext, tekstachteraf) = cursor2.fetchone()
            printMetRegels(tekstachteraf)
            xx =findMultiLineComments(tekstachteraf)
            print(xx)
        print('zoekterm: {0}, regelnummers: {1}'.format(zoekterm, regelnummers))


def findMultiLineComments(tekst):
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
    verzamel_alle_primitieven_per_file()