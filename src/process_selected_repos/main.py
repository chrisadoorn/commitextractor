import logging
import os
from datetime import datetime

from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, \
    ManualChecking
from src.repo_extractor.commitextractor import extract_repository
from src.requester.api_requester import fetch_authors_per_commit

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
                        ],
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


if __name__ == '__main__':
    try:
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        # create_tables()
        # GhSearchSampleRequester.get_sample('Elixir')
        # process_repos('Elixir')
        fetch_authors_per_commit(500)
        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
