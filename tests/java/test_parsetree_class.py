import os
import unittest

import antlr4
import pyparsing

from src.java_parsing.JavaLexer import JavaLexer
from src.java_parsing.JavaParser import JavaParser
from src.java_parsing.parsetree_searcher import find_class_use, to_nltk_tree


class Test(unittest.TestCase):

    @staticmethod
    def read_file(filename):
        filepath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../data/java/class', filename))
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

    def get_treestring_from_file(self, filepath: str) -> str:
        textafter = self.read_file(filepath)
        text = self.__remove_comments(textafter)
        inputstream = antlr4.InputStream(text)
        lexer = JavaLexer(inputstream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JavaParser(stream)
        parser.setTrace(True)
        tree = parser.compilationUnit()

        return tree.toStringTree(recog=parser)

    def test_not_used(self):
        tree_string = self.get_treestring_from_file('TestNotUsed.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertFalse(self, found, 'onterecht gebruik gevonden')

    def test_instance_declaration(self):
        tree_string = self.get_treestring_from_file('TestInstanceDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik instance declaration niet gevonden')

    def test_local_declaration(self):
        tree_string = self.get_treestring_from_file('TestLocalDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik local declaration niet gevonden')

    def test_parameter_declaration(self):
        tree_string = self.get_treestring_from_file('TestParameterDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als parameter niet gevonden')

    def test_generics_declaration(self):
        tree_string = self.get_treestring_from_file('TestGenericsDeclaration.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik als generic niet gevonden')

    def test_extends(self):
        tree_string = self.get_treestring_from_file('Testextends.java')
        ntlr_tree = to_nltk_tree(tree_string)
        found = find_class_use(ntlr_tree, 'Thread', False)
        unittest.TestCase.assertTrue(self, found, 'gebruik door extends niet gevonden')
