from peewee import CharField, Model, IntegerField, AutoField, BooleanField, BigIntegerField
from playhouse.postgres_ext import PostgresqlExtDatabase

from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlExtDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                              host=params.get('host'), port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = pg_db_schema


# bestandswijziging info krijgt zijn id van bestandswijziging.
class JavaParserSelection(BaseModel):
    class Meta:
        table_name = 'java_parser_selection_view'
    # id is het bwz id. peewee kan er niet tegen als een tabel geen id veld heeft.
    id = IntegerField()
    bw_id = IntegerField()
    commit_id = IntegerField()
    project_id = IntegerField()
    zoekterm = CharField()
    tekstvooraf = CharField()
    tekstachteraf = CharField()


class JavaParseResult(BaseModel):

    class Meta:
        table_name = 'java_parse_result'

    id = IntegerField(primary_key=True)
    zoekterm = CharField()
    bw_id = IntegerField()
    commit_id = IntegerField()
    is_gebruik = BooleanField()
    is_nieuw = BooleanField()
    is_verwijderd = BooleanField()
    bevat_unknown = BooleanField()
    usage_list_achteraf = CharField()
    usage_list_vooraf = CharField()

    # de constructie die hier gebruikt voor om een insert,
    # dan wel een update uit te voeren is specifiek voor gebruik in combinatie met postgresql
    # zie https://docs.peewee-orm.com/en/latest/peewee/querying.html ,zoek hier naar on_conflict
    def insert_or_update(bzw_id, zoekterm, bw_id, commit_id, is_gebruik, is_nieuw, is_verwijderd, bevat_unknown, usage_list_achteraf, usage_list_vooraf):
        JavaParseResult.insert(id=bzw_id, zoekterm=zoekterm, bw_id=bw_id, commit_id=commit_id, is_gebruik=is_gebruik,
                               is_nieuw=is_nieuw, is_verwijderd=is_verwijderd, bevat_unknown=bevat_unknown,
                               usage_list_achteraf=usage_list_achteraf, usage_list_vooraf=usage_list_vooraf).on_conflict(
            conflict_target=[JavaParseResult.id],  # Which constraint?
            preserve=[JavaParseResult.id],  # Use the value we would have inserted.
            update={JavaParseResult.zoekterm: zoekterm,
                    JavaParseResult.bw_id: bw_id,
                    JavaParseResult.commit_id: commit_id,
                    JavaParseResult.is_gebruik: is_gebruik,
                    JavaParseResult.is_nieuw: is_nieuw,
                    JavaParseResult.is_verwijderd: is_verwijderd,
                    JavaParseResult.bevat_unknown: bevat_unknown,
                    JavaParseResult.usage_list_achteraf: usage_list_achteraf,
                    JavaParseResult.usage_list_vooraf: usage_list_vooraf}).execute()


pg_db.connect()
