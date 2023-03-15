import logging
from datetime import datetime

from src import configurator
from src.experimental import commitextractor
from src.experimental.models import GhSearchSelection


def initialize():
    dt = datetime.now()
    logging.basicConfig(filename='../../log/main.' + str(dt) + '.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    configurator.inifile = '../../var/commitextractor.ini'


def execute(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.selected_for_survey,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null())
    for t in ghs.select():
        print(t.name)
        t.meta_import_started_at = datetime.now()
        commitextractor.extract_repository(t.name, t.id)
        t.meta_import_ready_at = datetime.now()
        t.save()


if __name__ == '__main__':
    initialize()
    execute('Java')
