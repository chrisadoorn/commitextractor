import logging
import os
from datetime import datetime

from peewee import fn

from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, \
    ManualChecking, CommitAuthorInformation, ProjectsProcessedForAuthors
from src.repo_extractor.commitextractor import extract_repository
from src.requester.api_requester import get_author_data

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
                         CommitAuthorInformation, ProjectsProcessedForAuthors],
                        safe=True)


def process_repos(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null()).order_by(
        fn.Random()).limit(1)

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
        t.selected_for_survey = True
        extract_repository(t.name, project.id)
        t.meta_import_ready_at = datetime.now()
        t.save()


def fetch_authors():
    cursor = pg_db.execute_sql(
        "SELECT p.naam, p.id , COALESCE(ppfa.processed,false) as processed  FROM test.project AS p " +
        "LEFT OUTER JOIN test.projectsprocessedforauthors AS ppfa ON (p.id = ppfa.project_id) " +
        "WHERE processed is null limit(10);"

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


if __name__ == '__main__':
    initialize()
    create_tables()
    # process_repos('Elixir')
    fetch_authors()
