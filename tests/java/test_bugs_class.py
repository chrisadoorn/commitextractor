import unittest

from src.java_parser.parsetree_searcher import find_class_use, to_nltk_tree
from tests.java.test_java_shared import get_treestring_from_file, get_class_usage

RELATIVE_PATH = '../data/java/bugs'


class Test(unittest.TestCase):

    def test_78260(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_78260.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Thread'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['instantation', 'static_use']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_57682(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_57682.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Flow'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['instance_variable', 'method_argument', 'instance_variable', 'method_argument',
                            'enum_declaration', 'constructor_declaration']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_81785(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_81785.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Flow'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['instance_variable', 'class_declaration']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_14057(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_14057.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Runnable'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['implements', 'type_declaration']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_56346(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_56346.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Condition'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['interface_definition', 'method_argument', 'method_argument', 'method_argument']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_8856(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_8856.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Thread'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['identifier']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_35261(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_35261.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'synchronized'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['blockstatement', 'blockstatement', 'blockstatement', 'blockstatement']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_1042198(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_1042198.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'synchronized'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['blockstatement']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_11079304(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_11079304.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Lock'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['import', 'annotation', 'annotation', 'annotation', 'type_declaration', 'annotation', 'type_declaration', 'annotation', 'type_declaration', 'annotation', 'type_declaration', 'annotation', 'type_declaration', 'annotation', 'type_declaration', 'annotation', 'type_declaration']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_340155(self):
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_340155.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'Thread'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['local_variable', 'instantation', 'static_use', 'identifier', 'identifier', 'local_variable', 'static_use', 'local_variable', 'static_use', 'local_variable', 'static_use', 'local_variable', 'static_use', 'local_variable', 'static_use']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    def test_1606748(self):
        # extends  java.util.TimerTask ipv extends TimerTask met een import van java.util.TimerTask
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_1606748.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'TimerTask'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['extends']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')

    @unittest.skip
    def test_477935(self):
        # classname wordt alleen genoemd. Heeft combinatie met parse error
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'bug_477935.java')
        ntlr_tree = to_nltk_tree(tree_string)
        zoekterm = 'ReentrantLock'

        results = get_class_usage(ntlr_tree, zoekterm)
        expected_results = ['import', 'piep']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')
