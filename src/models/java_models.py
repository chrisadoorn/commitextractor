from peewee import CharField, Model, IntegerField, BooleanField
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
    categorie = CharField()
    packagenaam = CharField()


class JavaParseResult(BaseModel):

    class Meta:
        table_name = 'java_parse_result'

    id = IntegerField(primary_key=True)
    zoekterm = CharField()
    bw_id = IntegerField()
    commit_id = IntegerField()
    is_in_namespace = BooleanField()
    is_gebruik_gewijzigd = BooleanField()
    is_nieuw = BooleanField()
    is_verwijderd = BooleanField()
    vooraf_usage_ontbreekt = BooleanField()
    achteraf_nieuw_usage = BooleanField()
    bevat_unknown = BooleanField()
    parse_error_vooraf = BooleanField()
    parse_error_achteraf = BooleanField()
    len_usage_vooraf = IntegerField()
    len_usage_achteraf = IntegerField()
    usage_list_achteraf = CharField()
    usage_list_vooraf = CharField()

    # de constructie die hier gebruikt voor om een insert,
    # dan wel een update uit te voeren is specifiek voor gebruik in combinatie met postgresql
    # zie https://docs.peewee-orm.com/en/latest/peewee/querying.html ,zoek hier naar on_conflict
    def insert_or_update(bzw_id, zoekterm, bw_id, commit_id, is_in_namespace, is_gebruik_gewijzigd, is_nieuw,
                         is_verwijderd, vooraf_usage_ontbreekt, achteraf_nieuw_usage, bevat_unknown, usage_list_achteraf, usage_list_vooraf
                         , parse_error_vooraf, parse_error_achteraf):
        JavaParseResult.insert(id=bzw_id, zoekterm=zoekterm, bw_id=bw_id, commit_id=commit_id, is_in_namespace=is_in_namespace,
                               is_gebruik_gewijzigd=is_gebruik_gewijzigd, is_nieuw=is_nieuw, is_verwijderd=is_verwijderd,
                               vooraf_usage_ontbreekt=vooraf_usage_ontbreekt, achteraf_nieuw_usage=achteraf_nieuw_usage,bevat_unknown=bevat_unknown,
                               len_usage_vooraf=len(usage_list_vooraf), len_usage_achteraf=len(usage_list_achteraf),
                               usage_list_achteraf=str(usage_list_achteraf), usage_list_vooraf=str(usage_list_vooraf),
                               parse_error_vooraf=parse_error_vooraf, parse_error_achteraf=parse_error_achteraf
        ).on_conflict(
            conflict_target=[JavaParseResult.id],  # Which constraint?
            preserve=[JavaParseResult.id],  # Use the value we would have inserted as key
            update={JavaParseResult.zoekterm: zoekterm,
                    JavaParseResult.bw_id: bw_id,
                    JavaParseResult.commit_id: commit_id,
                    JavaParseResult.is_in_namespace: is_in_namespace,
                    JavaParseResult.is_gebruik_gewijzigd: is_gebruik_gewijzigd,
                    JavaParseResult.is_nieuw: is_nieuw,
                    JavaParseResult.is_verwijderd: is_verwijderd,
                    JavaParseResult.vooraf_usage_ontbreekt: vooraf_usage_ontbreekt,
                    JavaParseResult.achteraf_nieuw_usage: achteraf_nieuw_usage,
                    JavaParseResult.bevat_unknown: bevat_unknown,
                    JavaParseResult.parse_error_vooraf: parse_error_vooraf,
                    JavaParseResult.parse_error_achteraf: parse_error_achteraf,
                    JavaParseResult.len_usage_vooraf: len(usage_list_vooraf),
                    JavaParseResult.len_usage_achteraf: len(usage_list_achteraf),
                    JavaParseResult.usage_list_achteraf: str(usage_list_achteraf),
                    JavaParseResult.usage_list_vooraf: str(usage_list_vooraf)}).execute()


pg_db.connect()
