
from peewee import PostgresqlDatabase
from src.models.models import BestandsWijziging
from src.models.analysis_models import Zoekterm
from src.models.analyzed_data_models import BestandsWijzigingZoekterm
from datetime import datetime

from src.utils.configurator import get_database_configuration

global db_connectie

def start_fill_analysis_table():

    for z in Zoekterm.select():
        print(datetime.now())
        a = 0
        for t in BestandsWijziging.select().where(BestandsWijziging.extensie == z.extensie,
                                                                      BestandsWijziging.difftext.contains(z.zoekwoord)):
                print("z.zoekwoord")
                print(z.zoekwoord)
                print("t.id")
                print(t.id)
                bestandswijzigingzoekterm = BestandsWijzigingZoekterm()
                bestandswijzigingzoekterm.idbestandswijziging = t.id
                bestandswijzigingzoekterm.zoekterm = z.zoekwoord
                bestandswijzigingzoekterm.save()
                a = a + 1
        print(datetime.now())
        print("aantal voorkomens keyword")
        print(a)

params = get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))

pg_db.connect()
start_fill_analysis_table()

if __name__ == '__main__':
    pg_db.create_tables(
        [BestandsWijzigingZoekterm],
        safe=True)
