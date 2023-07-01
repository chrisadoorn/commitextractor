from peewee import CharField, AutoField, BigIntegerField, IntegerField, BooleanField

from src.models.extracted_data_models import BaseModel, pg_db_schema, pg_database


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
    afkeurreden = CharField(null=True)
    aantalgevonden_oud = IntegerField(default=0)
    aantalgevonden_nieuw = IntegerField(default=0)


def get_voor_bestandswijziging(bestandswijzigings_id: int) -> (int, int, str, bool, str, int, int):
    sql = 'select id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw from ' + \
          pg_db_schema + '.bestandswijziging_zoekterm where idbestandswijziging = ' + str(bestandswijzigings_id)
    cursor = pg_database.execute_sql(sql)
    return cursor.fetchall()


class Zoekterm(BaseModel):
    extensie = CharField(null=True, max_length=20)
    zoekwoord = CharField(null=True)


class Regelnummer(BaseModel):
    class Meta:
        table_name = 'bestandswijziging_zoekterm_regelnummer'

    id = AutoField(primary_key=True)
    idbestandswijziging = BigIntegerField(null=False)
    zoekterm = CharField(null=False)
    regelnummer = IntegerField(null=False)
    regelsoort = CharField(null=False)


def delete_regelnummer_by_key(bestandswijzigings_id: int, zoekterm: str) -> None:
    """

    :param bestandswijzigings_id:
    :param zoekterm:
    """
    sql = 'delete from ' + pg_db_schema + '.bestandswijziging_zoekterm_regelnummer where idbestandswijziging = ' + \
          str(bestandswijzigings_id) + ' and zoekterm = \'' + zoekterm + '\''
    pg_database.execute_sql(sql)


def insert_regelnummers_by_key(bestandswijzigings_id: int, zoekterm: str, regelnummers: [int], regelsoort: str) -> None:
    """
    Wij gebruiken hier een postgresql functie, unnest, om in 1 keer eeen insert te doen voor alle elementen van de lijst regelnummers
    :param bestandswijzigings_id:
    :param zoekterm:
    :param regelnummers:
    :param regelsoort:
    """
    sql = 'insert into ' + pg_db_schema + '.bestandswijziging_zoekterm_regelnummer (idbestandswijziging, zoekterm, regelnummer, regelsoort) values( ' + \
          str(bestandswijzigings_id) + ',\'' + zoekterm + '\',unnest (ARRAY' + str(regelnummers) + '),\'' + regelsoort + '\')'
    pg_database.execute_sql(sql)

