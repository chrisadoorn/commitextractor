import unittest
import uuid
from src import configurator, db_postgresql

TEST_INI_FILE = 'var/test.ini'
TEST_ERROR_FILE = 'var/test_error.ini'


class Test(unittest.TestCase):
    # test of het aantal processen opgehaald kan worden
    def test_deregistreer_processor(self):
        identifier = str(uuid.uuid4())
        configurator.set_inifile(TEST_INI_FILE)
        db_postgresql.open_connection()
        verwacht = 0
        resultaat = db_postgresql.registreer_processor(identifier)
        unittest.TestCase.assertGreater(self, resultaat, verwacht, 'geen proces geregistreerd niet!')

        db_postgresql.deregistreer_processor(identifier)


