
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
        #possibletodo: clean up difftest - dependent on language
        for t in BestandsWijziging.select().where(BestandsWijziging.extensie == z.extensie,
                                                                      BestandsWijziging.difftext.contains(z.zoekwoord)):
                bestandswijzigingzoekterm = BestandsWijzigingZoekterm()
                bestandswijzigingzoekterm.idbestandswijziging = t.id
                bestandswijzigingzoekterm.zoekterm = z.zoekwoord
                bestandswijzigingzoekterm.save()
                a = a + 1
        print(datetime.now())
        print("aantal voorkomens keyword")
        print(a)

# clean up toml files (only keep concurrency package-dependencies declaration)
def clean_rust_toml(text):
    # strip line comment
    pos_comment = text.find('dependencies')
    if pos_comment > -1:
        text = text[pos_comment:]
    return text

def cleanupTableDifftext(extensie):
    connection = db_postgresql._get_connection()
    cursor1 = connection.cursor()

    sql_querydifftext = "select id, difftext from " + schema + ".bestandswijziging where extensie = '" + extensie + "'"
    print(sql_querydifftext)
    cursor1.execute(sql_querydifftext)

    cursor2 = connection.cursor()
    sql_update_difftext_tomlfiles = "UPDATE " + schema + ".bestandswijziging " + "set difftext= %s where id = %s"
    for z in cursor1.fetchall():
        cursor2.execute(sql_update_difftext_tomlfiles, (clean_rust_toml(z[1]), z[0]))
        connection.commit()
    connection.close()

if __name__ == '__main__':
    params = get_database_configuration()
    pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))


    pg_db.connect()
    #cleanupTableDifftext()
    start_fill_analysis_table()


