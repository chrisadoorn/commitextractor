from peewee import CharField, Model, DateTimeField, PostgresqlDatabase, TextField, BigIntegerField

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = params.get('schema')


class Analyse(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="analysis", on_delete="CASCADE", column_name="id")
    idcommit = ForeignKeyField(CommitInfo, backref="analysis", on_delete="CASCADE", column_name="id")
    idbestand = ForeignKeyField(BestandsWijziging, backref="analysis", on_delete="CASCADE", column_name="id")
    committer_name = ForeignKeyField(CommitInfo, backref="analysis", on_delete="CASCADE", column_name="username")
    committer_emailaddress = ForeignKeyField(CommitInfo, backref="analysis", on_delete="CASCADE",
                                             column_name="emailaddress")
    keyword = TextField(null=True)
    loc = IntegerField(null=True)

