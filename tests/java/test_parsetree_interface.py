import unittest

from src.java_parsing.parsetree_searcher import find_class_use, to_nltk_tree
from tests.java.test_java_shared import get_treestring_from_file

RELATIVE_PATH = '../data/java/interface'


class Test(unittest.TestCase):

    def test_not_used(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestNotUsed.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertFalse(self, found, 'onterecht gebruik gevonden')

    def test_instance_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestInstanceDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik instance declaration niet gevonden')

    def test_local_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestLocalDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik local declaration niet gevonden')

    def test_parameter_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestParameterDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als parameter niet gevonden')

    def test_generics_declaration(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestGenericsDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als generic niet gevonden')

    def test_implements(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImplements.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Runnable', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik door extends niet gevonden')
