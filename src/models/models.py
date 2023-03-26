from peewee import CharField, DateField, Model, AutoField, BooleanField, \
    IntegerField, DateTimeField, SQL, PostgresqlDatabase, TextField, BigIntegerField
# from playhouse.migrate import PostgresqlMigrator, migrate

from src import configurator

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))


class BaseModel(Model):
    class Meta:
        database = pg_db
        schema = 'test'


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


class CommitInformation(BaseModel):
    id = AutoField(primary_key=True)
    id_project = BigIntegerField(null=True)
    commit_date_time = DateTimeField(null=True)
    hash_value = CharField(max_length=40)
    username = CharField(null=True)
    email_address = CharField(null=True)
    remark = TextField(null=True)


class FileChanges(BaseModel):
    id = AutoField(primary_key=True)
    id_project = IntegerField(null=True)
    id_commit = BigIntegerField(null=True)
    filename = CharField(null=True, max_length=1024)
    location = CharField(null=True, max_length=1024)
    extension = CharField(null=True, max_length=64)
    diff_text = TextField(null=True)
    text_before = TextField(null=True)
    text_after = TextField(null=True)


class CommitInfo(BaseModel):
    id = AutoField(primary_key=True)
    idproject = BigIntegerField(null=True)
    commitdatumtijd = DateTimeField(null=True)
    hashvalue = CharField(null=True, max_length=40)
    username = CharField(null=True)
    emailaddress = CharField(null=True)
    remark = TextField(null=True)


class BestandsWijziging(BaseModel):
    id = AutoField(primary_key=True)
    idcommit = BigIntegerField(null=False)
    filename = CharField(null=True, max_length=512)
    locatie = CharField(null=True, max_length=512)
    extensie = CharField(null=True, max_length=20)
    difftext = TextField(null=True)
    tekstachteraf = TextField(null=True)

# migrator = PostgresqlMigrator(pg_db)
# selected_for_survey = BooleanField(null=True)
# meta_import_started_at = DateTimeField(null=True)
# meta_import_ready_at = DateTimeField(null=True)
#
# migrate(
#   migrator.set_search_path('test'),
#   migrator.add_column('ghsearchselection', 'selected_for_survey', selected_for_survey),
#   migrator.add_column('ghsearchselection', 'meta_import_started_at', meta_import_started_at),
#   migrator.add_column('ghsearchselection', 'meta_import_ready_at', meta_import_ready_at)
# )
#
