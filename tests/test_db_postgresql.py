import unittest
import uuid
import os
import sys

# test moet bestanden aanroepen met het relatieve pad ( from src)
# db_postgresql roept vervolgens configurator aan zonder pad. Omdat de context de testmap is,
# vindt db_postgresql vervolgens de configurator niet meer.
# onderstaand statement voegt de src toe als ezt=xtra, eerste locatie toe om in te zoeken.
# dit statement moet komen voordat de configurator en db_postgresql worden geimporteerd.
# N.B. Deze constructie is alleen nodig bij een test waarbij module getest wordt die een andere module nodig heeft.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# door bovenstaand statement hoef je hier geen from src meer te gebruiken, maar de IDE snapt dit niet.
# from src mag nog wel, dus dit gaat goed zonder foutmeldingen.
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
