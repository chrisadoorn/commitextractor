import unittest

from src.java_parsing.parsetree_searcher import find_class_use, to_nltk_tree, find_import
from tests.java.test_java_shared import get_treestring_from_file

RELATIVE_PATH = '../data/java/import'


class Test(unittest.TestCase):

    def test_not_used(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent', 'atomic', False)
        unittest.TestCase.assertFalse(self, found, 'onterecht gebruik gevonden')

    def test_import_by_name(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent','ConcurrentHashMap', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import by name niet gevonden')

    def test_import_by_wildcard(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent.locks', 'LockSupport', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import by wildcard niet gevonden')

    def test_same_package(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent.atomic', 'AtomicLong', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik same package niet gevonden')
