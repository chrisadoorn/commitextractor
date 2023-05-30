from peewee import CharField, DateField, Model, AutoField, BooleanField, IntegerField, DateTimeField, SQL, \
    PostgresqlDatabase, TextField, BigIntegerField, ForeignKeyField

from src.models.extracted_data_models import BestandsWijziging
from src.utils import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                           host=params.get('host'), port=params.get('port'))
pg_db_schema = params.get('schema')


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = params.get('schema')


class GhSearchSelection(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=True)
    is_fork = BooleanField(null=True)
    commits = IntegerField(null=True)
    branches = IntegerField(null=True)
    default_branch = CharField(null=True)
    releases = IntegerField(null=True)
    contributors = IntegerField(null=True)
    license = CharField(null=True)
    watchers = IntegerField(null=True)
    stargazers = IntegerField(null=True)
    forks = IntegerField(null=True)
    size = BigIntegerField(null=True)
    created_at = DateTimeField(null=True)
    pushed_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)
    homepage = CharField(null=True)
    main_language = CharField(null=True)
    total_issues = IntegerField(null=True)
    open_issues = IntegerField(null=True)
    total_pull_requests = IntegerField(null=True)
    open_pull_requests = IntegerField(null=True)
    last_commit = DateTimeField(null=True)
    last_commit_sha = CharField(null=True)
    has_wiki = BooleanField(null=True)
    is_archived = BooleanField(null=True)
    import_date = DateField(null=True, constraints=[SQL('DEFAULT CURRENT_DATE')])
    sub_study = CharField(null=True)
    selected_for_survey = BooleanField(null=True)
    meta_import_started_at = DateTimeField(null=True)
    meta_import_ready_at = DateTimeField(null=True)


class TempDiffTextAnalysis(BaseModel):
    id = AutoField(primary_key=True)
    idbestandswijziging = ForeignKeyField(BestandsWijziging, backref="temp_diff_text_analyses", on_delete="CASCADE",
                                          column_name="idbestandswijziging")
    filename = CharField(null=True, max_length=512)
    location = CharField(null=True, max_length=512)
    line_number = IntegerField(null=True)
    line_text = TextField(null=True)
    primitives = TextField(null=True)
    type_of_diff = IntegerField(null=True)
    project_name = CharField(null=False)
    author_id = IntegerField(null=False)
    commitdatumtijd = DateTimeField(null=True)
