import unittest

import antlr4
import pyparsing
from antlr4 import ParseTreeWalker
# from treelib import Node, Tree
from nltk import Tree

from src.java_parsing.CustomJavaParserListener import CustomJavaParserListener
from src.java_parsing.JavaLexer import JavaLexer
from src.java_parsing.JavaParser import JavaParser
from src.java_parsing.parsetree_searcher import find_class_use

IS_GEIMPORTEERD = 0
IS_INSTANCE_DECL = 1
IS_LOCAL_DECL = 2
IS_ARGUMENT = 3
IS_RESULT = 4
IS_PARAM = 5
IS_USED = 6


class Test(unittest.TestCase):

    @staticmethod
    def read_file(filepath):
        file = open(filepath, 'rt')
        text = file.read()
        file.close()
        return text

    @staticmethod
    def __remove_comments(text):
        # single line comments removed //
        comment_filter = pyparsing.dblSlashComment.suppress()
        # multiline comments removed /*...*/
        comment_filter2 = pyparsing.cppStyleComment.suppress()
        newtext = comment_filter.transformString(text)
        newtext2 = comment_filter2.transformString(newtext)
        return newtext2

    def get_tree_from_file(self, filepath):
        textafter = self.read_file(filepath)
        text = self.__remove_comments(textafter)
        inputstream = antlr4.InputStream(text)
        lexer = JavaLexer(inputstream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JavaParser(stream)
        parser.setTrace(True)
        tree = parser.compilationUnit()
        print('********** compilationUnit ****************************************')
        print(tree.toStringTree(recog=parser))
        print('******************************************************')

        return tree

    def get_treestring_from_file(self, filepath):
        textafter = self.read_file(filepath)
        text = self.__remove_comments(textafter)
        inputstream = antlr4.InputStream(text)
        lexer = JavaLexer(inputstream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JavaParser(stream)
        parser.setTrace(True)
        tree = parser.compilationUnit()

        return tree.toStringTree(recog=parser)

    def test_import(self):
        tree = self.get_tree_from_file('../data/java/import/TestImport.java')
        walker = ParseTreeWalker()
        expected = 'import \n'

        t_listener = CustomJavaParserListener( zoekterm='ConcurrentHashMap', packagenaam='java.util.concurrent',
                                               zoekmethode='class', output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'import bij naam niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')

        t_listener = CustomJavaParserListener(zoekterm='Condition', packagenaam='java.util.concurrent.locks', zoekmethode='class', output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'import met * niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')

        t_listener = CustomJavaParserListener(zoekterm='AtomicLong', packagenaam='java.util.concurrent.atomic',
                                              zoekmethode='class', output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'is hetzelfde package niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')

    def test_class_usage(self):
        tree = self.get_tree_from_file('../data/java/class/TestInstanceDeclaration.java')
        tree_string = self.get_treestring_from_file('../data/java/class/TestInstanceDeclaration.java')
        ntlr_tree = Tree.fromstring(tree_string, '()')

        found = find_class_use(ntlr_tree, 'Thread', False)

        unittest.TestCase.assertTrue(self, found, 'gebruik class niet gevonden')

        walker = ParseTreeWalker()
        expected = 'TypeType Thread\n'

        t_listener = CustomJavaParserListener(zoekterm='Thread', packagenaam='java.lang', zoekmethode='class',
                                              output='')
        #        walker.walk(listener=t_listener, t=tree)

        var = t_listener.is_gevonden_in()
        # thread mag niet geimporteerd zijn, want dan is het een andere namespace
        unittest.TestCase.assertTrue(self, not var[IS_GEIMPORTEERD], 'import bij naam niet gevonden')
