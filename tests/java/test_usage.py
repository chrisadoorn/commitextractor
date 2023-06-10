import unittest

from src.java_parsing.java_tree_analyzer import determine_searchword_usage
from src.java_parsing.parsetree_searcher import to_nltk_tree, leaves_with_path
from tests.java.test_java_shared import get_treestring_from_file

RELATIVE_PATH = '../data/java/class'


class Test(unittest.TestCase):

    def test_usage(self):
        zoekterm = 'Thread'
        tree_string = get_treestring_from_file(RELATIVE_PATH, 'TestClassUsage.java')
        ntlr_tree = to_nltk_tree(tree_string)

        leaves_path = leaves_with_path(ntlr_tree, ['complilationUnit'])
        usage_paths = []
        for path in leaves_path:
            path.reverse()  # eerste term wordt het zoekwoord.
            if path[0] == zoekterm:
                usage_paths.append(path)

        results = determine_searchword_usage(usage_paths, zoekterm)
        print(str(results))
        expected_results = ['import', 'extends', 'instance_variable', 'instantation', 'method_result', 'method_argument'
            , 'method_typeargument', 'local_variable', 'instantation', 'instantation', 'generics extend', 'extends']
        unittest.TestCase.assertEqual(self, expected_results, results, 'onverwachte resultaten gevonden')
