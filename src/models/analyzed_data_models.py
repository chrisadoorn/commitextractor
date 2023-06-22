import playhouse
from peewee import CharField, Model, AutoField, BigIntegerField, IntegerField, BooleanField
from playhouse.postgres_ext import PostgresqlExtDatabase

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlExtDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                              host=params.get('host'), port=params.get('port'), autoconnect=False)
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

    # de constructie die hier gebruikt voor om een insert,
    # dan wel een update uit te voeren is specifiek voor gebruik in combinatie met postgresql
    # zie https://docs.peewee-orm.com/en/latest/peewee/querying.html ,zoek hier naar on_conflict
    def insert_or_update(parameter_id, regels_oud, regels_nieuw):
        BestandsWijzigingInfo.insert(id=parameter_id, regels_oud=regels_oud, regels_nieuw=regels_nieuw).on_conflict(
            conflict_target=[BestandsWijzigingInfo.id],  # Which constraint?
            preserve=[BestandsWijzigingInfo.id],  # Use the value we would have inserted.
            update={BestandsWijzigingInfo.regels_oud: regels_oud,
                    BestandsWijzigingInfo.regels_nieuw: regels_nieuw}).execute()


# voor gebruik van het integer array field zie
# https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#postgres-ext-api-notes
class BestandsWijzigingZoekterm(BaseModel):
    class Meta:
        table_name = 'bestandswijziging_zoekterm'

    id = AutoField(primary_key=True)
    idbestandswijziging = BigIntegerField(null=False)
    zoekterm = CharField(null=False)
    falsepositive = BooleanField(default=False)
    regelnummers = playhouse.postgres_ext.ArrayField(field_class=IntegerField)
    aantalgevonden = IntegerField(default=0)

    def get_voor_bestandswijziging(bestandswijzigings_id):
        sql = 'select id, idbestandswijziging, zoekterm, falsepositive, regelnummers, aantalgevonden  from ' + \
              pg_db_schema + '.bestandswijziging_zoekterm where idbestandswijziging = ' + str(bestandswijzigings_id)
        cursor = pg_db.execute_sql(sql)
        return cursor.fetchall()


class Zoekterm(BaseModel):
    extensie = CharField(null=True, max_length=20)
    zoekwoord = CharField(null=True)


pg_db.connect()
