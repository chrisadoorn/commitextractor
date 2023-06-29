import unittest

from src.java_parser import java_parser


class Test(unittest.TestCase):

    def test_empty_lists(self):
        vooraf = []
        achteraf = []
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertFalse(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertFalse(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertFalse(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_empty_vooraf(self):
        vooraf = []
        achteraf = ['import']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertFalse(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertTrue(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_empty_achteraf(self):
        vooraf = ['import']
        achteraf = []
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertTrue(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertFalse(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_vooraf_ontbreekt(self):
        vooraf = ['import', 'extends']
        achteraf = ['import']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertTrue(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertFalse(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_nieuw_toegevoegd(self):
        vooraf = ['import']
        achteraf = ['import', 'extends']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertFalse(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertTrue(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_vooraf_ontbreekt_zelfde_keyword(self):
        vooraf = ['import', 'import']
        achteraf = ['import']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertTrue(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertFalse(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_nieuw_toegevoegd_zelfde_keyword(self):
        vooraf = ['import']
        achteraf = ['import', 'import']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertFalse(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertTrue(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')

    def test_beide_soorten_wijzigingen(self):
        vooraf = ['import', 'extends', 'extends']
        achteraf = ['import', 'import', 'extends']
        (vooraf_usage_ontbreekt, achteraf_nieuw_usage, gewijzigd) = java_parser.compare_usage(vooraf, achteraf)
        unittest.TestCase.assertTrue(self, vooraf_usage_ontbreekt, 'onverwachte resultaten: vooraf_usage_ontbreekt')
        unittest.TestCase.assertTrue(self, achteraf_nieuw_usage, 'onverwachte resultaten: achteraf_nieuw_usage')
        unittest.TestCase.assertTrue(self, gewijzigd, 'onverwachte resultaten: gewijzigd')
