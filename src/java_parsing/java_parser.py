import antlr4
import antlr4.error
import pyparsing
import logging
from datetime import datetime

from antlr4 import ParseTreeWalker

from src.java_parsing.CustomJavaParserListener import CustomJavaParserListener
from src.java_parsing.JavaLexer import JavaLexer
from src.java_parsing.JavaParser import JavaParser
from src.java_parsing.JavaParserListener import JavaParserListener
from src.utils import db_postgresql
from src.models.analyzed_data_models import BestandsWijzigingZoekterm
from src.models.extracted_data_models import BestandsWijziging


def __remove_comments(text):
    # single line comments removed //
    comment_filter = pyparsing.dblSlashComment.suppress()
    # multiline comments removed /*...*/
    comment_filter2 = pyparsing.cppStyleComment.suppress()
    newtext = comment_filter.transformString(text)
    newtext2 = comment_filter2.transformString(newtext)
    return newtext2


def __analyze_by_project(projectnaam, projectid):
    start = datetime.now()
    logging.info('start verwerking (' + str(projectid) + '):  ' + projectnaam + str(start))

    # haal per bestandswijzigingszoekterm, die niet eerder als false positive is herkend, de textafter op
    bw_list = BestandsWijziging().select().where(BestandsWijziging.id == 20214)
    for bw in bw_list:
        textafter = bw.tekstachteraf
        # verwijder alle comments.
        text = __remove_comments(textafter)
        inputstream = antlr4.InputStream(text)
        lexer = JavaLexer(inputstream)
        stream = antlr4.CommonTokenStream(lexer)
        parser = JavaParser(stream)
        parser.setTrace(True)
        tree = parser.compilationUnit()
        rc_listener = CustomJavaParserListener(zoekterm='ResultCode', packagenaam='org.prebid.mobile', output='')
        t_listener = CustomJavaParserListener(zoekterm='Thread', packagenaam='java.lang', output='')
        walker = ParseTreeWalker()
        resultaat = walker.walk(listener=rc_listener, t=tree)
        var = rc_listener.is_gevonden_in()
        print('rc_listener : ' + str(var))
        resultaat = walker.walk(listener=t_listener, t=tree)
        var = t_listener.is_gevonden_in()
        print('t_listener : ' + str(var))

        # is zoekterm daadwerkelijk gebruikt? (afhankelijk van soort zoekwoord hoe dit bepaald wordt. kijk naar indicatie booleans. )
        # is zoekterm anders gebruikt dan in textvooraf? vergelijk listener outputs
        # vergelijk resultaat pre en after

    eind = datetime.now()
    logging.info('einde verwerking ' + projectnaam + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectnaam + ' duurde ' + str(duur))
    print(duur)


def analyze(process_identifier):
    oude_processtap = 'zoekterm_controleren'
    nieuwe_processtap = 'java_parsing'

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
                __analyze_by_project(projectnaam, projectid)
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
