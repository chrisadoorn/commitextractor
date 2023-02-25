import logging
import unittest
from src import configurator, load_ghsearch


class Test(unittest.TestCase):

    def test_ghsearch(self):
        # initialiseer logging
        logging.basicConfig(filename='../log/test_ghsearch.log',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            level=logging.INFO, encoding='utf-8')
        logging.info('starting test')
        configurator.set_inifile('var/test.ini')
        load_ghsearch.load()
