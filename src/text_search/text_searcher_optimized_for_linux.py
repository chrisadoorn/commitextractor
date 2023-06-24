import logging

from src.models.analyzed_data_models import Zoekterm
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration
from src.utils.db_postgresql import _get_new_connection

"""De globale variabelen db_connectie, zoekterm_list en DBConnectionPool zijn verwijderd, omdat ze niet nodig zijn.
Query's met parameters in plaats van strings aan elkaar te rijgen om de uitvoering van query's te verbeteren.
Gebruik van een contextmanager (with) voor databaseverbindingen om een goed beheer van bronnen te garanderen.
Gebruik van meer beschrijvende namen voor variabelen om de leesbaarheid van de code te verbeteren."""

def __get_zoektermen_list():
    """
    Retrieves list of configured search terms.
    :return: List of Zoekterm objects
    """
    return Zoekterm.select().execute()

def __get_bestandswijzigingen_list(zoekterm, project_id, connection):
    """
    Retrieves the list of bestandswijzigingen for a project containing a certain keyword.
    :param zoekterm: Zoekterm object
    :param project_id: Project ID
    :param connection: Database connection
    :return: List of tuples, where each tuple contains the ID of a bestandswijziging
    """
    sql = (
        "SELECT b.id FROM " + schema + ".bestandswijziging b, "
        + schema + ".commitinfo c WHERE b.idcommit = c.id AND c.idproject = %s "
        "AND b.extensie = %s AND b.difftext LIKE %s"
    )
    params = (project_id, zoekterm.extensie, f"%{zoekterm.zoekwoord}%")
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as e:
        logging.exception(e)

def __find_zoektermen(project_id, zoektermen, project_naam, process_identifier):
    """
    Searches for a project, for each zoekterm all bestandswijzigingen containing this zoekterm.
    :param project_id: Project ID
    :param zoektermen: List of Zoekterm objects
    :param project_naam: Project name
    :param process_identifier: Process identifier
    """
    connection = _get_connection_from_pool(process_identifier)
    for zoekterm in zoektermen:
        count = 0
        for (bw_id,) in __get_bestandswijzigingen_list(zoekterm, project_id, connection):
            save_bestandswijziging_zoekterm(connection, bw_id, zoekterm.zoekwoord)
            count += 1
        logging.debug(f"{project_naam} bevat zoekterm {zoekterm.zoekwoord}: {count}")

def search_by_project(process_identifier):
    """
    Searches projects for configured zoektermen.
    :param process_identifier: Process identifier
    """
    oude_processtap = "identificatie"
    nieuwe_processtap = "zoekterm_vinden"
    try:
        db_connectie = _get_connection_from_pool(process_identifier)
        db_postgresql.registreer_processor(process_identifier, db_connectie)
        volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap, db_connectie)
        while volgend_project[2] == 1:
            projectnaam, projectid, rowcount = volgend_project[1], volgend_project[0], volgend_project[2]
            verwerking_status = "mislukt"
            try:
                __find_zoektermen(project_id=projectid, zoektermen=__get_zoektermen_list(),
                                  project_naam=projectnaam, process_identifier=process_identifier)
                verwerking_status = "verwerkt"
            except Exception as e_inner:
                logging.error("Er zijn fouten geconstateerd tijdens de verwerking van het project. Zie details hieronder")
                logging.exception(e_inner)

            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid,
                                                connection=db_connectie)
            volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap, db_connectie)

        db_postgresql.deregistreer_processor(process_identifier, db_connectie)

    except Exception as e_outer:
        logging.error("Er zijn fouten geconstateerd tijdens het loopen door de projectenlijst. Zie details hieronder")
        logging.exception(e_outer)

def _get_connection_from_pool(process_identifier):
    return _get_new_connection()

def save_bestandswijziging_zoekterm(connection, idbestandswijziging, zoekterm):
    sql = (
        "INSERT INTO " + schema + ".bestandswijziging_zoekterm (idbestandswijziging, zoekterm) "
        "VALUES (%s, %s)"
    )
    params = (idbestandswijziging, zoekterm)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            connection.commit()
    except Exception as e:
        logging.exception(e)
