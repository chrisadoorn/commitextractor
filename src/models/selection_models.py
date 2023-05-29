from peewee import CharField, DateField, Model, AutoField, BooleanField, IntegerField, SQL, \
    PostgresqlDatabase, TextField, BigIntegerField, ForeignKeyField

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                           host=params.get('host'), port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = params.get('schema')


class Selectie(BaseModel):
    id = AutoField(primary_key=True)
    selectionmoment = DateField(null=False, constraints=[SQL('DEFAULT CURRENT_DATE')])
    language = CharField(null=True)
    commitsminimum = IntegerField(null=True)
    contributorsminimum = IntegerField(null=True)
    excludeforks = BooleanField(null=True)
    onlyforks = BooleanField(null=True)
    hasissues = BooleanField(null=True)
    haspulls = BooleanField(null=True)
    haswiki = BooleanField(null=True)
    haslicense = BooleanField(null=True)
    committedmin = DateField(null=True)


class Project(BaseModel):
    id = AutoField(primary_key=True)
    naam = CharField(null=True)
    idselectie = ForeignKeyField(Selectie, backref="projects", column_name="idselectie")
    main_language = CharField(null=True)
    is_fork = BooleanField(null=True)
    license = CharField(null=True)
    forks = IntegerField(null=True)
    contributors = IntegerField(null=True)
    project_size = BigIntegerField(null=True)
    create_date = DateField(null=True)
    last_commit = DateField(null=True)
    number_of_languages = IntegerField(null=True)
    languages = TextField(null=True)
    aantal_commits = IntegerField(null=True)
