import logging
from src.author_identifier import api_requester
from src.utils import db_postgresql

FAILURE_MSG = 'Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder'
PROCESSED = 'verwerkt'
FAILURE = 'mislukt'
IDENTIFICATION = 'identificatie'
EXTRACTION = 'extractie'


def identify_by_project(process_identifier: str) -> None:
    """
    :param process_identifier:
    """
    oude_processtap = EXTRACTION
    nieuwe_processtap = IDENTIFICATION

    try:
        db_postgresql.open_connection()
        db_postgresql.registreer_processor(process_identifier)

        volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
        rowcount = volgend_project[2]
        while rowcount == 1:
            projectnaam = volgend_project[1]
            projectid = volgend_project[0]
            verwerking_status = FAILURE

            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                api_requester.fetch_authors_by_project(projectid=projectid)
                verwerking_status = PROCESSED
            # continue processing next project
            except Exception as e_inner:
                logging.error(FAILURE_MSG)
                logging.exception(e_inner)

            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid)
            volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
            rowcount = volgend_project[2]

        # na de loop
        db_postgresql.deregistreer_processor(process_identifier)

    except Exception as e_outer:
        logging.error(FAILURE_MSG)
        logging.exception(e_outer)



