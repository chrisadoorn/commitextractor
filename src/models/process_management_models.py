from peewee import CharField, Model, DateTimeField, PostgresqlDatabase, TextField, BigIntegerField

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = params.get('schema')


class Verwerk_Project(BaseModel):
    id = BigIntegerField(primary_key=True)
    naam = CharField(null=False)
    start_extractie = DateTimeField(null=True)
    einde_extractie = DateTimeField(null=True)
    processor = CharField(null=True)
    status = CharField(null=True)
    resultaat = TextField(null=True)


pg_db.connect()
