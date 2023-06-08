import os

import antlr4
import pyparsing

from src.java_parsing.JavaLexer import JavaLexer
from src.java_parsing.JavaParser import JavaParser


def __read_file(relative_path, filename):
    filepath = os.path.realpath(os.path.join(os.path.dirname(__file__), relative_path, filename))
    file = open(filepath, 'rt')
    text = file.read()
    file.close()
    return text
def __remove_comments(text):
    # single line comments removed //
    comment_filter = pyparsing.dblSlashComment.suppress()
    # multiline comments removed /*...*/
    comment_filter2 = pyparsing.cppStyleComment.suppress()
    newtext = comment_filter.transformString(text)
    newtext2 = comment_filter2.transformString(newtext)
    return newtext2


def get_treestring_from_file(relative_path: str, filepath: str) -> str:
    textafter = __read_file(relative_path, filepath)
    text = __remove_comments(textafter)
    inputstream = antlr4.InputStream(text)
    lexer = JavaLexer(inputstream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(stream)
    parser.setTrace(True)
    tree = parser.compilationUnit()

    return tree.toStringTree(recog=parser)