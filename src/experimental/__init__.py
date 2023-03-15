import logging
from datetime import datetime

from peewee import fn

from src import configurator
from src.experimental import commitextractor
from src.experimental.models import GhSearchSelection


def initialize():
    dt = datetime.now()
    logging.basicConfig(filename='log/main.' + str(dt) + '.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    configurator.inifile = 'config.ini'


def execute(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null()).order_by(
        fn.Random()).limit(5)

    for t in ghs.select():
        print(t.name)
        t.meta_import_started_at = datetime.now()
        t.selected_for_survey = True
        commitextractor.extract_repository(t.name, t.id)
        t.meta_import_ready_at = datetime.now()
        t.save()


if __name__ == '__main__':
    initialize()
    execute('Elixir')
