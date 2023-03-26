import logging
from datetime import datetime
from peewee import fn
from src.processes.commitextractor import extract_repository
from src.models.models import GhSearchSelection, pg_db, CommitInformation, FileChanges, CommitInfo, BestandsWijziging

def initialize():
    dt = datetime.now()
    logging.basicConfig(filename='../log/main.' + str(dt) + '.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def create_tables():
    pg_db.create_tables([GhSearchSelection, CommitInformation, FileChanges,CommitInfo,BestandsWijziging], safe=True)


def execute(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null()).order_by(
        fn.Random()).limit(1)

    for t in ghs.select():
        print(t.name)
        t.meta_import_started_at = datetime.now()
        t.selected_for_survey = True
        extract_repository(t.name, t.id)
        t.meta_import_ready_at = datetime.now()
        t.save()


if __name__ == '__main__':
    initialize()
    create_tables()
    execute('Elixir')
