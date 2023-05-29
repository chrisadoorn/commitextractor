import playhouse
from peewee import CharField, Model, AutoField, BigIntegerField, IntegerField, BooleanField, DateTimeField, \
    ForeignKeyField, TextField
from playhouse.postgres_ext import PostgresqlExtDatabase

from src.models.selection_models import Project
from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlExtDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                              host=params.get('host'), port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = pg_db_schema


class ManualChecking(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="manual_checkings", on_delete="CASCADE", column_name="idproject")
    comment = TextField(null=True)
    type_of_project = CharField(null=True)
    exclude = BooleanField(null=True)
    exclude_reason = CharField(null=True)


class Handmatige_Check(BaseModel):
    id = AutoField(primary_key=True)
    projectnaam = CharField(null=False)
    project_id = BigIntegerField
    bwz_id = BigIntegerField(null=False)
    zoekterm = CharField(null=False)
    falsepositive = BooleanField(null=False)
    regelnummers = playhouse.postgres_ext.ArrayField(field_class=IntegerField)
    bestandswijziging_id = BigIntegerField(null=False)
    commit_datum = DateTimeField(null=False)
    commit_sha = CharField(null=False)
    commit_remark = CharField(null=True)
    gecontroleerd = BooleanField(null=True)
    akkoord = BooleanField(null=True)
    opmerking = CharField(null=True)


pg_db.connect()
