from peewee import CharField, Model, AutoField, DateTimeField, TextField, ForeignKeyField, IntegerField
from playhouse.pool import PooledPostgresqlExtDatabase

from src.models.selection_models import Project
from src.utils import configurator

params = configurator.get_database_configuration()

pg_database = PooledPostgresqlExtDatabase(
    database=params.get('database'),
    max_connections=32,
    stale_timeout=300,
    user=params.get('user'),
    password=params.get('password'),
    host=params.get('host'),
    port=params.get('port'))

pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_database
        schema = pg_db_schema


class CommitInfo(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="commits", on_delete="CASCADE", column_name="idproject")
    commitdatumtijd = DateTimeField(null=True)
    hashvalue = CharField(null=True, max_length=40)
    username = CharField(null=True)
    emailaddress = CharField(null=True)
    remark = TextField(null=True)
    author_id = IntegerField(null=True)


class BestandsWijziging(BaseModel):
    id = AutoField(primary_key=True)
    idcommit = ForeignKeyField(CommitInfo, backref="bestandsWijzigingen", on_delete="CASCADE", column_name="idcommit")
    filename = CharField(null=True)
    locatie = CharField(null=True)
    extensie = CharField(null=True)
    difftext = TextField(null=True)
    tekstachteraf = TextField(null=True)
    tekstvooraf = TextField(null=True)


def open_connection():
    pg_database.connect()


def close_connection():
    pg_database.close()
