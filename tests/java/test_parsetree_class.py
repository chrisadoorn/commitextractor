import unittest

from src.java_parsing.parsetree_searcher import find_class_use, to_nltk_tree
from tests.java.test_java_shared import get_treestring_from_file, get_class_usage

ZOEKTERM = 'Thread'

RELATIVE_PATH = '../data/java/class'


class Test(unittest.TestCase):

    def test_not_used(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestNotUsed.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertFalse(self, found, 'onterecht gebruik gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        unittest.TestCase.assertTrue(self, len(results) == 0, 'onverwachte resultaten gevonden')

    def test_instance_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestInstanceDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik instance declaration niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['instance_variable', 'instantation']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_local_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestLocalDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik local declaration niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['local_variable', 'instantation']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_local_variable(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestLocalVariable.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik local variable niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['local_variable']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_parameter_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestParameterDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als parameter niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['method_argument']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_generics_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestGenericsDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als generic niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['method_typeargument']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_extends(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestExtends.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, ZOEKTERM, False)
        unittest.TestCase.assertTrue(self, found, 'gebruik door extends niet gevonden')

        results = get_class_usage(ntlr_tree, ZOEKTERM)
        expected_results = ['extends']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')
