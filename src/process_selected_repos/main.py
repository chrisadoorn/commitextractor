import logging
import os
from datetime import datetime

from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, \
    ManualChecking, CommitAuthorInformation, ProjectsProcessedForAuthors, ProjectAuthorInformation, pg_db_schema
from src.repo_extractor.commitextractor import extract_repository
from src.requester.api_requester import get_author_data, get_author_data_one_commit

dt = datetime.now()
filename = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '..', '..', 'log', 'main.' + str(dt) + '.log'))


def initialize():
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def create_tables():
    pg_db.create_tables([GhSearchSelection, Selectie, Project, CommitInfo, BestandsWijziging, ManualChecking,
                         CommitAuthorInformation, ProjectsProcessedForAuthors, ProjectAuthorInformation],
                        safe=True)


def process_repos(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null())

    selection = Selectie()
    selection.language = subproject
    selection.save()

    for t in ghs.select():
        project = Project()
        project.naam = t.name
        project.idselectie = selection.id
        project.main_language = t.main_language
        project.is_fork = t.is_fork
        project.license = t.license
        project.forks = t.forks
        project.contributors = t.contributors
        project.project_size = t.size
        project.create_date = t.created_at
        project.last_commit = t.last_commit
        project.number_of_languages = 0
        project.languages = ""
        project.aantal_commits = t.commits
        project.save()

        print(t.name)
        t.meta_import_started_at = datetime.now()

        try:
            extract_repository(t.name, project.id)
            t.selected_for_survey = True
        except Exception as e:
            t.selected_for_survey = False
            print(e)
        t.meta_import_ready_at = datetime.now()
        t.save()


def fetch_authors_all_commits(limit=10):
    schema = pg_db_schema
    cursor = pg_db.execute_sql(
        "SELECT p.naam, p.id , COALESCE(ppfa.processed,false) as processed  FROM " + schema + ".project AS p " +
        "LEFT OUTER JOIN " + schema + ".projectsprocessedforauthors AS ppfa ON (p.id = ppfa.project_id) " +
        "WHERE processed is null limit({});".format(limit)
    )
    for (project_naam, project_id, processed) in cursor.fetchall():
        data = get_author_data(project_naam)
        for (commit_sha, author_login, author_id) in data[0]:
            print(commit_sha, author_login, author_id)
            commit_author = CommitAuthorInformation()
            commit_author.sha = commit_sha
            commit_author.project_name = project_naam
            commit_author.author_login = author_login
            commit_author.author_id = author_id
            if not CommitAuthorInformation().select().where(
                    CommitAuthorInformation.sha == commit_sha, CommitAuthorInformation.project_name == project_naam) \
                    .exists():
                commit_author.save()
        processed = ProjectsProcessedForAuthors()
        processed.project_name = project_naam
        processed.project_id = project_id
        processed.processed = True
        processed.error_description = data[1]
        processed.save()


def fetch_authors_per_project(limit=5):
    schema = pg_db_schema
    cursor = pg_db.execute_sql(
        "SELECT p.naam, p.id , COALESCE(ppfa.processed,false) as processed  FROM " + schema + ".project AS p " +
        "LEFT OUTER JOIN " + schema + ".projectsprocessedforauthors AS ppfa ON (p.id = ppfa.project_id) " +
        "WHERE processed is null limit({});".format(limit)
    )
    for (project_naam, project_id, processed) in cursor.fetchall():
        cursor2 = pg_db.execute_sql(
            "SELECT ci.emailaddress, ci.username, ci.hashvalue FROM " + schema + ".commitinfo AS ci " +
            "WHERE idproject = {};".format(project_id)
        )
        error = ''
        for (emailaddress_hashed, username_hashed, sha) in cursor2.fetchall():
            load_data = False
            project_author_information = ProjectAuthorInformation()
            try:
                pai = ProjectAuthorInformation().select().where(
                    ProjectAuthorInformation.project_name == project_naam,
                    ProjectAuthorInformation.emailaddress_hashed == emailaddress_hashed,
                    ProjectAuthorInformation.username_hashed == username_hashed).get()
                if pai.author_id < 0:
                    load_data = True
                    project_author_information = pai
            except ProjectAuthorInformation.DoesNotExist:
                load_data = True
            if load_data:
                (commit_sha, author_login, author_id), error = get_author_data_one_commit(project_naam, sha)
                project_author_information.project_name = project_naam
                project_author_information.emailaddress_hashed = emailaddress_hashed
                project_author_information.username_hashed = username_hashed
                project_author_information.author_login = author_login
                project_author_information.author_id = author_id
                project_author_information.save()
            else:
                print('Already processed:' + project_naam + ', ea:' + emailaddress_hashed + ', us: ' + username_hashed)

        processed = ProjectsProcessedForAuthors()
        processed.project_name = project_naam
        processed.project_id = project_id
        processed.processed = True
        processed.error_description = error
        processed.save()


def fetch_authors_per_commit(limit=5):
    schema = pg_db_schema
    cursor = pg_db.execute_sql(
        "SELECT ci.idproject, ci.emailaddress, ci.username, ci.hashvalue, pr.naam "
        "FROM " + schema + ".commitinfo AS ci " +
        "JOIN " + schema + ".project AS pr ON ci.idproject = pr.id " +
        "WHERE author_id is null limit({});".format(limit)
    )
    for (id_project, email_address_hashed, username_hashed, sha, project_name) in cursor.fetchall():
        try:
            existing_commit_info = CommitInfo().select().where(
                CommitInfo.idproject == id_project,
                CommitInfo.username == username_hashed,
                CommitInfo.emailaddress == email_address_hashed,
                CommitInfo.author_id.is_null(False)).get()
            print(
                "[update] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            update_commit_info(id_project, sha, existing_commit_info.author_id, existing_commit_info.author_login)
        except CommitInfo.DoesNotExist:
            print("[New] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            (commit_sha, author_login, author_id), error = get_author_data_one_commit(project_name, sha)
            update_commit_info(id_project, sha, author_id, author_login)


def update_commit_info(id_project, sha, author_id, author_login):
    to_update_commit_info = CommitInfo().select().where(
        CommitInfo.idproject == id_project, CommitInfo.hashvalue == sha).get()
    to_update_commit_info.author_id = author_id
    to_update_commit_info.author_login = author_login
    to_update_commit_info.save()


if __name__ == '__main__':
    try:
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        create_tables()
        # GhSearchSampleRequester.get_sample('Elixir')
        # process_repos('Elixir')
        fetch_authors_per_commit(1000)
        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
