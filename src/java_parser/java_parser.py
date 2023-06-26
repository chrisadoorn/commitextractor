import logging
from datetime import datetime

import antlr4
import antlr4.error
import pyparsing
from nltk import Tree

from src.java_parser import parsetree_searcher
from src.java_parser.JavaLexer import JavaLexer
from src.java_parser.JavaParser import JavaParser
from src.java_parser.java_tree_analyzer import determine_searchword_usage
from src.java_parser.parsetree_searcher import to_nltk_tree, leaves_with_path
from src.models.java_models import JavaParserSelection, JavaParseResult
from src.utils import db_postgresql

PROCESSTAP = 'java_parsing'
STATUS_MISLUKT = 'mislukt'
STATUS_VERWERKT = 'verwerkt'


def __remove_comments(text):
    # single line comments removed //
    comment_filter = pyparsing.dblSlashComment.suppress()
    # multiline comments removed /*...*/
    comment_filter2 = pyparsing.cppStyleComment.suppress()
    newtext = comment_filter.transformString(text)
    newtext2 = comment_filter2.transformString(newtext)
    return newtext2


def __get_treestring(text: str) -> str:
    inputstream = antlr4.InputStream(text)
    lexer = JavaLexer(inputstream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(stream)
    parser.setTrace(False)  # toggle trace logging to standard out
    tree = parser.compilationUnit()

    return tree.toStringTree(recog=parser)


def __usage_is_same(usage_list_vooraf: [str], usage_list_achteraf: [str]) -> bool:
    """
    Het gebruik vooraf en achteraf is gelijk als dezelfde vorm van gebruik even vaak gebruikt wordt.
    :param usage_list_vooraf: list of strings indicating usage in text before
    :param usage_list_achteraf: list of strings indicating usage in text after
    :return bool: True is lists contain the same items
    """
    if len(usage_list_vooraf) != len(usage_list_achteraf):
        return False
    if len(usage_list_vooraf) == 0:
        return False

    work_vooraf = usage_list_vooraf.copy()
    work_vooraf.sort()
    work_achteraf = usage_list_achteraf.copy()
    work_achteraf.sort()
    return all(x == y for x, y in zip(work_vooraf, work_achteraf))


def __analyze_project(projectnaam, projectid):
    start = datetime.now()
    logging.info('start verwerking (' + str(projectid) + '):  ' + projectnaam)

    vorig_bw_id = 0

    selection_list = JavaParserSelection.select().where(JavaParserSelection.project_id == projectid).order_by(
        JavaParserSelection.bw_id)
    for listitem in selection_list:
        zoekterm = listitem.zoekterm
        packagenaam = listitem.packagenaam
        import_controle = listitem.import_controle
        commit_id = listitem.commit_id
        bw_id = listitem.bw_id
        bzw_id = listitem.id
        tekstvooraf = listitem.tekstvooraf
        tekstachteraf = listitem.tekstachteraf
        is_nieuw = (tekstvooraf is None)
        is_verwijderd = (tekstachteraf is None)
        is_in_gebruik = False
        is_gebruik_gewijzigd = False
        usage_list_vooraf = []
        usage_list_achteraf = []

        if vorig_bw_id != bw_id:
            # maak nieuwe parsetrees
            try:
                if not is_nieuw:
                    temp_vooraf = __get_treestring(tekstvooraf)
                    vooraf_tree = to_nltk_tree(temp_vooraf)
                else:
                    vooraf_tree = to_nltk_tree('()')

                if not is_verwijderd:
                    tempachteraf = __get_treestring(tekstachteraf)
                    achteraf_tree = to_nltk_tree(tempachteraf)
                else:
                    achteraf_tree = to_nltk_tree('()')
            except ValueError as e:
                # Na een exception in dit deel werken we door om alle andere bestandswijzingen in het project te verwerken.
                # we loggen de fout, met de bestandswijziging id, zodat wij eventueel kunnen uitzoeken wat het probleem is.
                logging.error('Parse exception in bestandswijziging ' + str(bw_id))
                logging.error(e)
                continue

        if is_verwijderd:
            # hele bestand verwijderen telt niet als gebruik
            is_gebruik_gewijzigd = False
            is_in_gebruik = False
        else:
            # parsetree content voor zoekterm achteraf
            usage_list_achteraf = __get_usage_zoekterm(achteraf_tree, zoekterm)
            is_in_gebruik = is_in_correct_namespace(achteraf_tree, packagenaam, zoekterm, import_controle)

            if not is_nieuw:
                usage_list_vooraf = __get_usage_zoekterm(vooraf_tree, zoekterm)
                is_gebruik_gewijzigd = not __usage_is_same(usage_list_vooraf, usage_list_achteraf)
            else:
                is_gebruik_gewijzigd = len(usage_list_achteraf) > 0

        bevat_unknown = 'unknown' in usage_list_vooraf or 'unknown' in usage_list_achteraf
        if bevat_unknown:
            logging.warning('Unknown in tekst bestandswijziging ' + str(bw_id) + ' zoekwoord= ' + zoekterm)

        # persist resultaat
        JavaParseResult.insert_or_update(bzw_id=bzw_id, zoekterm=zoekterm, bw_id=bw_id, commit_id=commit_id,
                                         is_in_gebruik=is_in_gebruik, is_gebruik_gewijzigd=is_gebruik_gewijzigd,
                                         is_nieuw=is_nieuw, is_verwijderd=is_verwijderd,
                                         bevat_unknown=bevat_unknown, usage_list_achteraf=str(usage_list_achteraf),
                                         usage_list_vooraf=str(usage_list_vooraf))

        vorig_bw_id = bw_id

    eind = datetime.now()
    logging.info('einde verwerking ' + projectnaam + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectnaam + ' duurde ' + str(duur))
    print(duur)


def is_in_correct_namespace(tree: Tree, packagenaam: str, zoekterm: str, import_required: bool) -> bool:
    """
    import required  is_imported  result
        True            True       True     : imported or in same package
        True            False      False    : Zoekterm is in different package
        False           True       True     : import unneccessarily done (java.lang)
        False           False      True     : import not needed (java.lang or keyword)

    :param tree:
    :param packagenaam: packagename of the zoekterm
    :param zoekterm: gezocht woord
    :param import_required: boolean: yes if the zoekterm must be imported, or in the same package.
    :return: boolean
    """
    is_imported = parsetree_searcher.find_import(tree, packagenaam, zoekterm, False)
    return not import_required or (import_required and is_imported)


def __get_usage_zoekterm(achteraf_tree, zoekterm):
    leaves_path = leaves_with_path(achteraf_tree, ['complilationUnit'])
    usage_paths = []
    for path in leaves_path:
        path.reverse()  # eerste term wordt het zoekwoord.
        if path[0] == zoekterm:
            usage_paths.append(path)
    usage_list = determine_searchword_usage(usage_paths, zoekterm)

    return usage_list


def analyze(process_identifier, oude_processtap):
    nieuwe_processtap = PROCESSTAP

    try:
        db_postgresql.open_connection()
        db_postgresql.registreer_processor(process_identifier)

        volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
        rowcount = volgend_project[2]
        while rowcount == 1:
            projectnaam = volgend_project[1]
            projectid = volgend_project[0]
            verwerking_status = 'mislukt'

            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                __analyze_project(projectnaam, projectid)
                verwerking_status = 'verwerkt'
            # continue processing next project
            except Exception as e_inner:
                logging.error('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
                logging.exception(e_inner)

            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid)
            volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
            rowcount = volgend_project[2]

        # na de loop
        db_postgresql.deregistreer_processor(process_identifier)

    except Exception as e_outer:
        logging.error('Er zijn fouten geconstateerd tijdens het loopen door de projectenlijst. Zie details hieronder')
        logging.exception(e_outer)
