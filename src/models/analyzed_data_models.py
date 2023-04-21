import playhouse
from peewee import CharField, Model, AutoField, DateTimeField, PostgresqlDatabase, TextField, BigIntegerField, \
    IntegerField, ForeignKeyField, BooleanField
from playhouse.postgres_ext import PostgresqlExtDatabase

from src.models.extracted_data_models import BestandsWijziging
from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlExtDatabase('multicore', user=params.get('user'), password=params.get('password'),
                              host=params.get('host'), port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = pg_db_schema


# bestandswijziging info krijgt zijn id van bestandswijziging.
class BestandsWijzigingInfo(BaseModel):
    class Meta:
        table_name = 'bestandswijziging_info'

    id = BigIntegerField(primary_key=True)
    regels_oud = IntegerField(default=0)
    regels_nieuw = IntegerField(default=0)


# voor gebruik van het integer field zie https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#postgres-ext-api-notes
class BestandsWijzigingZoekterm(BaseModel):
    class Meta:
        table_name = 'bestandswijziging_zoekterm'

    id = AutoField(primary_key=True)
    idbestandswijziging = ForeignKeyField(BestandsWijziging, backref="bestandswijziging_zoekterm", on_delete="CASCADE",
                                          column_name="idbestandswijziging"),
    zoekterm = CharField(null=False),
    falsepositive = BooleanField(default=False)
    regelnummers = playhouse.postgres_ext.ArrayField(field_class=IntegerField)
    aantalgevonden = IntegerField(default=0)


pg_db.connect()
