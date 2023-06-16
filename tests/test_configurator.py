import unittest
from src.utils import configurator

TEST_INI_FILE = 'var/test.ini'
TEST_ERROR_FILE = 'var/test_error.ini'


class Test(unittest.TestCase):
    # test of het aantal processen opgehaald kan worden
    def test_number_of_processes(self):
        configurator.set_inifile(TEST_INI_FILE)
        verwacht = 17
        resultaat = configurator.get_number_of_processes()
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'aantal processen matchen niet!')

    # test of er een exception komt als het aantal processen niet opgehaald kan worden
    def test_number_of_processes_error(self):
        configurator.set_inifile(TEST_ERROR_FILE)
        self.assertRaises(Exception, configurator.get_number_of_processes)

    # test of de database configuratie opgehaald kan worden
    def test_database_configuration(self):
        configurator.set_inifile(TEST_INI_FILE)
        resultaat = configurator.get_database_configuration()
        unittest.TestCase.assertEqual(self, 6, len(resultaat), 'aantal database parameters matchen niet!')

    # test of er een exception komt als het aantal processen niet opgehaald kan worden
    def test_number_of_processes_error(self):
        configurator.set_inifile(TEST_ERROR_FILE)
        self.assertRaises(Exception, configurator.get_database_configuration)

    # test of een import lijst opgehaald kan worden
    def test_ghsearch_importfile(self):
        configurator.set_inifile(TEST_INI_FILE)
        verwacht = 'data/test_ghsearch.json'
        resultaat = configurator.get_ghsearch_importfile()
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'ghsearch importfile niet correct!')

    # test of er een exception komt als de import lijst niet opgehaald kan worden
    def test_ghsearch_importfile_error(self):
        configurator.set_inifile(TEST_ERROR_FILE)
        self.assertRaises(Exception, configurator.get_ghsearch_importfile)

    # test of een import lijst gewenst is
    def test_ghsearch_importfile(self):
        configurator.set_inifile(TEST_INI_FILE)
        verwacht = 'data/test_ghsearch.json'
        resultaat = configurator.get_ghsearch_importfile()
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'ghsearch importfile niet correct!')

    # tests get_module_configurationitem
    def test_module_configurationitem_no_such_item(self):
        configurator.set_inifile(TEST_INI_FILE)
        self.assertRaises(Exception, configurator.get_module_configurationitem, 'load_ghsearch', 'bestaat_niet')

    def test_module_configurationitem(self):
        configurator.set_inifile(TEST_INI_FILE)
        verwacht = 'INFO'
        resultaat = configurator.get_module_configurationitem('load_ghsearch', 'loglevel')
        unittest.TestCase.assertEqual(self, verwacht, resultaat, 'ghsearch get module_configurationitem niet correct!')