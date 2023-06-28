import logging
import os
import unittest

import antlr4

from src.java_parser.JavaLexer import JavaLexer
from src.java_parser.JavaParser import JavaParser
from src.java_parser.java_parser import analyseer_parsetrees
from src.java_parser.parsetree_searcher import find_class_use, to_nltk_tree
from src.models.java_models import JavaParserSelection

# Deze file is om te controleren of onverwachte uitkomsten klopten.
# Zo is het mogelijk een enkel record te replayen.

def get_treestring(text: str) -> str:
    inputstream = antlr4.InputStream(text)
    lexer = JavaLexer(inputstream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(stream)
    parser.setTrace(False)  # toggle trace logging to standard out
    tree = parser.compilationUnit()

    return tree.toStringTree(recog=parser)


def init():
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log', 'test_analysis.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def perform_analysis(search_id):
    selection_list = JavaParserSelection.select().where(JavaParserSelection.id == search_id)
    for listitem in selection_list:
        zoekterm = listitem.zoekterm
        packagenaam = listitem.packagenaam
        categorie = listitem.categorie
        commit_id = listitem.commit_id
        bw_id = listitem.bw_id
        bzw_id = listitem.id
        tekstvooraf = listitem.tekstvooraf
        tekstachteraf = listitem.tekstachteraf
        is_nieuw = (tekstvooraf is None)
        is_verwijderd = (tekstachteraf is None)

        # maak nieuwe parsetrees
        try:
            if not is_nieuw:
                temp_vooraf = get_treestring(tekstvooraf)
                vooraf_tree = to_nltk_tree(temp_vooraf)
            else:
                vooraf_tree = to_nltk_tree('()')

            if not is_verwijderd:
                tempachteraf = get_treestring(tekstachteraf)
                achteraf_tree = to_nltk_tree(tempachteraf)
            else:
                achteraf_tree = to_nltk_tree('()')
        except ValueError as e:
            # Na een exception in dit deel werken we door om alle andere bestandswijzingen in het project te verwerken.
            # we loggen de fout, met de bestandswijziging id, zodat wij eventueel kunnen uitzoeken wat het probleem is.
            logging.error('Parse exception in bestandswijziging ' + str(bw_id))
            logging.error(e)
            continue

        analyseer_parsetrees(achteraf_tree, bw_id, bzw_id, categorie, commit_id, is_nieuw, is_verwijderd, packagenaam, vooraf_tree, zoekterm)


class Test(unittest.TestCase):

    @unittest.skip
    def test_4710(self):
        init()
        search_id = 4710
        perform_analysis(search_id)

    @unittest.skip
    def test_5489(self):
        init()
        search_id = 5489
        perform_analysis(search_id)

    @unittest.skip
    def test_10327(self):
        init()
        search_id = 10327
        perform_analysis(search_id)

    @unittest.skip
    def test_32302(self):
        init()
        search_id = 32302
        perform_analysis(search_id)

    @unittest.skip
    def test_32894(self):
        init()
        search_id = 32894
        perform_analysis(search_id)



