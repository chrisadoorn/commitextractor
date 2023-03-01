import unittest
import uuid

from src import db_postgresql, configurator, load_ghsearch

TEST_INI_FILE = 'var/test_vraag_volgend_project.ini'


def initialiseer_testset():
    identifier = str(uuid.uuid4())
    configurator.set_inifile(TEST_INI_FILE)
    db_postgresql.open_connection()
    db_postgresql.clean_testset()
    db_postgresql.registreer_processor(identifier)
    load_ghsearch.load()
    return identifier


def initialiseer_connectie():
    db_postgresql.open_connection()


class Test(unittest.TestCase):
    def test_set_van_drie(self):
        identifier = initialiseer_testset()
        initialiseer_connectie()

        # eerste record
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')
        id_1 = resultaat[0]
        naam_1 = resultaat[1]
        # tweede record
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')  # add assertion here
        id_2 = resultaat[0]
        naam_2 = resultaat[1]
        # derde record
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 1, 'onverwachte rowcount')  # add assertion here
        id_3 = resultaat[0]
        naam_3 = resultaat[1]
        # vierde record, niet meer aanwezig
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here
        # assert dat verschillende waardes zijn opgehaald.
        unittest.TestCase.assertTrue(self, (id_1 != id_2) and (id_1 != id_3) and (id_2 != id_3),
                                     'dezelfde waarde voor id wordt opgehaald')
        unittest.TestCase.assertTrue(self, (naam_1 != naam_2) and (naam_1 != naam_3) and (naam_2 != naam_3),
                                     'dezelfde waarde voor naam wordt opgehaald')

    def test_identifier_ontbreekt_in_db(self):
        initialiseer_connectie()
        identifier = str(uuid.uuid4())
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here

    def test_identifier_onjuiste_status(self):
        initialiseer_connectie()
        identifier = str(uuid.uuid4())
        db_postgresql.registreer_processor(identifier)
        db_postgresql.deregistreer_processor(identifier)
        resultaat = db_postgresql.volgend_project(processor=identifier)
        unittest.TestCase.assertEqual(self, resultaat[2], 0, 'onverwachte rowcount')  # add assertion here
