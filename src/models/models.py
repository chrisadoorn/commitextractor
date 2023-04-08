from peewee import CharField, DateField, Model, AutoField, BooleanField, \
    IntegerField, DateTimeField, SQL, PostgresqlDatabase, TextField, BigIntegerField, ForeignKeyField

from src.utils import configurator


params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase('multicore', user=params.get('user'), password=params.get('password'),
                           host='localhost', port=params.get('port'))


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


class ManualChecking(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="manual_checkings", on_delete="CASCADE", column_name="idproject")
    comment = TextField(null=True)
    type_of_project = CharField(null=True)
    exclude = BooleanField(null=True)
    exclude_reason = CharField(null=True)


class CommitInfo(BaseModel):
    id = AutoField(primary_key=True)
    idproject = ForeignKeyField(Project, backref="commits", on_delete="CASCADE", column_name="idproject")
    commitdatumtijd = DateTimeField(null=True)
    hashvalue = CharField(null=True, max_length=40)
    username = CharField(null=True)
    emailaddress = CharField(null=True)
    remark = TextField(null=True)


class BestandsWijziging(BaseModel):
    id = AutoField(primary_key=True)
    idcommit = ForeignKeyField(CommitInfo, backref="bestands_wijzigingen", on_delete="CASCADE", column_name="idcommit")
    filename = CharField(null=True, max_length=512)
    locatie = CharField(null=True, max_length=512)
    extensie = CharField(null=True, max_length=20)
    difftext = TextField(null=True)
    tekstachteraf = TextField(null=True)


class CommitAuthorInformation(BaseModel):
    id = AutoField(primary_key=True)
    sha = CharField(null=False, max_length=40, index=True)
    project_name = CharField(null=False, index=True)
    author_login = CharField(null=False)
    author_id = IntegerField(null=False)


class ProjectsProcessedForAuthors(BaseModel):
    id = AutoField(primary_key=True)
    project_name = CharField(null=False)
    project_id = ForeignKeyField(Project, backref="projects_processed_for_authors", on_delete="CASCADE",
                                 column_name="project_id")
    date_time = DateField(null=False, constraints=[SQL('DEFAULT CURRENT_DATE')])
    processed = BooleanField(null=False, default=False)
    error_description = TextField(null=True)

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
