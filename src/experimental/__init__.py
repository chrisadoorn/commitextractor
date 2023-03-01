import logging
from datetime import datetime

from src import configurator
from src.experimental.models import GhSearchSelection


def initialize():
    dt = datetime.now()
    logging.basicConfig(filename='../log/main.' + str(dt) + '.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    configurator.inifile = '../../var/commitextractor.ini'


def execute():
    ghs = GhSearchSelection.get(GhSearchSelection.id == 1)
    print(ghs.name)


if __name__ == '__main__':
    initialize()
    execute()
