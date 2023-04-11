
from peewee import PostgresqlDatabase
from src.models.analysis_models import Analyse
from src.models.models import BestandsWijziging
from src.utils import configurator
from datetime import datetime

from src.utils.configurator import get_database_configuration

global db_connectie

def create_tables():
    pg_db.create_tables([Analyse], safe=True)

def start_fill_analysis_table():

    keywords = configurator.get_keywords()

    for x in range(len(keywords)):
        print(keywords[x])
        print(datetime.now())
        for t in BestandsWijziging.select().where(BestandsWijziging.difftext.contains(keywords[x])):
                analyse = Analyse()
                analyse.idproject_id = t.idcommit.idproject
                #print(analyse.idproject_id )
                analyse.idcommit_id = t.idcommit
                analyse.idbestand_id = t.id
                analyse.committer_name = t.idcommit.username
                analyse.committer_emailaddress = t.idcommit.emailaddress
                analyse.keyword = keywords[x]
                # LoC tellen misschien via ModifiedFile nloc: Lines Of Code (LOC) of the file???
                analyse.loc = 0
                analyse.save()
        print(datetime.now())

params = get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))
create_tables()
start_fill_analysis_table()

