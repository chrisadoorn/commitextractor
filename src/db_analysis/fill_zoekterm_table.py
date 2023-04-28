
from peewee import PostgresqlDatabase
from src.models.analysis_models import Zoekterm
from src.utils import configurator, read_diff_rust
from datetime import datetime

from src.utils.configurator import get_database_configuration

global db_connectie


def start_fill_zoekterm_table():

    keywords = configurator.get_keywords()

    for x in range(len(keywords) -1):
        print(x)
        zoekterm = Zoekterm()
        zoekterm.extensie = keywords[0]
        zoekterm.zoekwoord = keywords[x+1]
        print(keywords[x+1])
        zoekterm.save()

    keywords_lib = configurator.get_keywords_lib()

    for x in range(len(keywords_lib) -1):
        print(x)
        zoekterm = Zoekterm()
        zoekterm.extensie = keywords_lib[0]
        zoekterm.zoekwoord = keywords_lib[x+1]
        print(keywords_lib[x+1])
        zoekterm.save()

params = get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))

start_fill_zoekterm_table()