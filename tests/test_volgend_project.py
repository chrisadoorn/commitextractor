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

from src.selection_loader import load_ghsearch
from src.utils import configurator, db_postgresql

TEST_INI_FILE = 'var/test_vraag_volgend_project.ini'


def initialiseer_testset():
    identifier = str(uuid.uuid4())
    configurator.set_inifile(TEST_INI_FILE)
    db_postgresql.open_connection()
    db_postgresql.clean_testset()
    db_postgresql.registreer_processor(identifier)
    load_ghsearch.load_importfile(configurator.get_ghsearch_importfile())
    initialiseer_connectie()  # load ghsearch stopt de connectie.
    return identifier


def initialiseer_connectie():
    db_postgresql.open_connection()


class Test(unittest.TestCase):
    def test_set_van_drie(self):
        identifier = initialiseer_testset()
        oude_processtap = 'selectie'
        nieuwe_processtap = 'test'

        # eerste record
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')
        id_1 = resultaat[0]
        naam_1 = resultaat[1]
        # tweede record
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')  # add assertion here
        id_2 = resultaat[0]
        naam_2 = resultaat[1]
        # derde record
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')  # add assertion here
        id_3 = resultaat[0]
        naam_3 = resultaat[1]
        # vierde record, niet meer aanwezig
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here
        # assert dat verschillende waardes zijn opgehaald.
        unittest.TestCase.assertTrue(self, (id_1 != id_2) and (id_1 != id_3) and (id_2 != id_3),
                                     'dezelfde waarde voor id wordt opgehaald')
        unittest.TestCase.assertTrue(self, (naam_1 != naam_2) and (naam_1 != naam_3) and (naam_2 != naam_3),
                                     'dezelfde waarde voor naam wordt opgehaald')

    def test_identifier_ontbreekt_in_db(self):
        initialiseer_connectie()
        identifier = str(uuid.uuid4())
        oude_processtap = 'selectie'
        nieuwe_processtap = 'test'
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here

    def test_identifier_onjuiste_status(self):
        initialiseer_connectie()
        identifier = str(uuid.uuid4())
        oude_processtap = 'selectie'
        nieuwe_processtap = 'test'
        db_postgresql.registreer_processor(identifier)
        db_postgresql.deregistreer_processor(identifier)
        resultaat = db_postgresql.volgend_project(identifier, oude_processtap, nieuwe_processtap)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here
