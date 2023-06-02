import unittest

import antlr4
import pyparsing
from antlr4 import ParseTreeWalker

from src.java_parsing.CustomJavaParserListener import CustomJavaParserListener
from src.java_parsing.JavaLexer import JavaLexer
from src.java_parsing.JavaParser import JavaParser

IS_GEIMPORTEERD = 0


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
        return tree


    def test_thread(self):
        tree = self.get_tree_from_file('data/java/jlt_thread.java')
        t_listener = CustomJavaParserListener(zoekterm='Thread', packagenaam='java.lang', output='')
        walker = ParseTreeWalker()
        resultaat = walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        print('t_listener : ' + str(var))

    def test_import(self):
        tree = self.get_tree_from_file('data/java/TestImport.java')
        walker = ParseTreeWalker()
        expected = 'import \n'

        t_listener = CustomJavaParserListener(zoekterm='ConcurrentHashMap', packagenaam='java.util.concurrent',
                                              output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'import bij naam niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')

        t_listener = CustomJavaParserListener(zoekterm='Condition', packagenaam='java.util.concurrent.locks', output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'import met * niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')

        t_listener = CustomJavaParserListener(zoekterm='AtomicLong', packagenaam='java.util.concurrent.atomic',
                                              output='')
        walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        unittest.TestCase.assertTrue(self, var[IS_GEIMPORTEERD], 'is hetzelfde package niet gevonden')
        unittest.TestCase.assertEqual(self, expected, t_listener.output, 'verschil in resultaat ')
