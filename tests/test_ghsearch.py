import logging
import unittest

from src import load_ghsearch
from src.utils import configurator


class Test(unittest.TestCase):

    def test_ghsearch(self):
        # initialiseer logging
        logging.basicConfig(filename='../log/test_ghsearch.log',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            level=logging.INFO, encoding='utf-8')
        logging.info('starting test')
        configurator.set_inifile('var/test.ini')
        # vraag max id op van selectie en project
        load_ghsearch.load_importfile(configurator.get_ghsearch_importfile())
        # vraag max id op van selectie en project
        #   dit moet bij beide 1 hoger zijn
        #   vraag record selectie op. controleer de inhoud
        #   vraag record project op.  controleer de inhoud
