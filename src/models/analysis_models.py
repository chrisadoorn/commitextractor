from peewee import *
from src.models.models import Project, CommitInfo, BestandsWijziging
from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))

class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = params.get('schema')

class Zoekterm(BaseModel):
    extensie = CharField(null=True, max_length=20)
    zoekwoord = CharField(null=True)

pg_db.connect()