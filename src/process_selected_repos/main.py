import logging
import os
from datetime import datetime
from peewee import fn
from src.processes.commitextractor import extract_repository
from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project

dt = datetime.now()
filename = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '..', '..', 'log', 'main.' + str(dt) + '.log'))


def initialize():
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def create_tables():
    pg_db.create_tables([GhSearchSelection, Selectie, Project, CommitInfo, BestandsWijziging], safe=True)


def execute(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null()).order_by(
        fn.Random()).limit(5)

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
        project.commits = t.commits
        project.save()
        print(t.name)
        t.meta_import_started_at = datetime.now()
        t.selected_for_survey = True
        extract_repository(t.name, project.id, extended=True)
        t.meta_import_ready_at = datetime.now()
        t.save()


if __name__ == '__main__':
    initialize()
    create_tables()
    execute('Elixir')
