import unittest

from src.java_parser.parsetree_searcher import to_nltk_tree, find_import, find_import_library
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

    def test_import_by_partial_name(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util','Collections.synchronizedList', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import by partial name niet gevonden')

    def test_import_by_wildcard(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent.locks', 'LockSupport', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import by wildcard niet gevonden')

    def test_static_import(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent.locks', 'LockSupport', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import by wildcard niet gevonden')

    def test_same_package(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import(ntlr_tree, 'java.util.concurrent.atomic', 'AtomicLong', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik same package niet gevonden')

    def test_import_library(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import_library(ntlr_tree, 'org.awaitility', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import library niet gevonden')
    def test_import_library_static(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestImport.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_import_library(ntlr_tree, 'com.lmax', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik import static library niet gevonden')
