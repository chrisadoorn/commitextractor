from peewee import CharField, Model, AutoField, DateTimeField, PostgresqlDatabase, TextField, BigIntegerField

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = pg_db_schema


class CommitInfo(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="idproject")
    commitdatumtijd = DateTimeField(null=True)
    hashvalue = CharField(null=True, max_length=40)
    username = CharField(null=True)
    emailaddress = CharField(null=True)
    remark = TextField(null=True)


class BestandsWijziging(BaseModel):
    id = AutoField(primary_key=True)
    idcommit = ForeignKeyField(CommitInfo, backref="idcommit")
    filename = CharField(null=True, max_length=512)
    locatie = CharField(null=True, max_length=512)
    extensie = CharField(null=True, max_length=20)
    difftext = TextField(null=True)
    tekstachteraf = TextField(null=True)


pg_db.connect()
