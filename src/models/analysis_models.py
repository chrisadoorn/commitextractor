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


class Analyse(BaseModel):
    idproject = ForeignKeyField(Project, backref='id')
    idcommit = ForeignKeyField(CommitInfo, backref="analysis")
    idbestand = ForeignKeyField(BestandsWijziging, backref="analysis")
    committer_name = ForeignKeyField(CommitInfo, backref="analysis", field="username")
    committer_emailaddress = ForeignKeyField(CommitInfo, backref="analysis", field ="emailaddress")
    keyword = TextField(null=True)
    loc = IntegerField(null=True)

pg_db.connect()