import os

import antlr4
from nltk import Tree

from src.java_parser.JavaLexer import JavaLexer
from src.java_parser.JavaParser import JavaParser
from src.java_parser.java_tree_analyzer import determine_searchword_usage
from src.java_parser.parsetree_searcher import leaves_with_path


def __read_file(relative_path, filename):
    filepath = os.path.realpath(os.path.join(os.path.dirname(__file__), relative_path, filename))
    file = open(filepath, 'rt')
    text = file.read()
    file.close()
    return text


def get_treestring_from_file(relative_path: str, filepath: str) -> str:
    textafter = __read_file(relative_path, filepath)
    inputstream = antlr4.InputStream(textafter)
    lexer = JavaLexer(inputstream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(stream)
    parser.setTrace(True)
    tree = parser.compilationUnit()

    return tree.toStringTree(recog=parser)


def get_class_usage(ntlr_tree: Tree, zoekterm: str) -> list[str]:
    leaves_path = leaves_with_path(ntlr_tree, ['complilationUnit'])
    usage_paths = []
    for path in leaves_path:
        path.reverse()  # eerste term wordt het zoekwoord.
        if path[0] == zoekterm:
            usage_paths.append(path)
            print(str(path))
    results = determine_searchword_usage(usage_paths, zoekterm)
    return results
