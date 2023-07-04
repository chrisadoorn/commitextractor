import logging

from src.models.analyzed_data_models import Zoekterm
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration

schema = get_database_configuration().get('schema')
zoekterm_list = []


def __get_zoektermen_list() -> [Zoekterm]:
    """
    Retrieves list of configured searchterms.
    :return: lijst van Zoekterm objecten
    """
    global zoekterm_list
    zoekterm_list = Zoekterm.select().execute()
    return zoekterm_list


def __get_bestandswijzigingen_list(zoekterm: Zoekterm, project_id: int) -> [(int,)]:
    """
    retrieves the list of bestandswijzigingen for a project containing a certain keyword.
    :param zoekterm: Zoekterm object
    :param project_id:
    :return: List of tuples, the first element containing the id of a bestandswijzigng
    """
    sql = "select b.id from " + schema + ".bestandswijziging b, " + schema + ".commitinfo c where b.idcommit = c.id and c.idproject = " + str(
        project_id) + " and   b.extensie = '" + zoekterm.extensie + "' and b.difftext like '%" + zoekterm.zoekwoord + "%'"
    try:
        cursor = db_postgresql.get_connection().cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        logging.exception(e)


# update table bestandswijziging_zoekterm when keyword is found
def __find_zoektermen(project_id: int, zoektermen: [Zoekterm], project_naam: str) -> None:
    """
    Searches for a project, for each zoekterm all bestandswijzigingen containing this zoekterm
    :param project_id:
    :param zoektermen:
    :param project_naam:
    """
    for zoekterm in zoektermen:
        a = 0
        for (bw_id,) in __get_bestandswijzigingen_list(zoekterm, project_id):
            save_bestands_wijziging_zoekterm(bw_id, zoekterm.zoekwoord)
            a = a + 1
        logging.debug('{0} bevat zoekterm {1} : {2}'.format(project_naam, zoekterm.zoekwoord, str(a)))


def search_by_project(process_identifier: str) -> None:
    """
    :rtype: None
    :param process_identifier:
    """

    oude_processtap = 'identificatie'
    nieuwe_processtap = 'zoekterm_vinden'
    try:
        global zoekterm_list
        __get_zoektermen_list()

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
                __find_zoektermen(project_id=projectid, zoektermen=zoekterm_list, project_naam=projectnaam)
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


def save_bestands_wijziging_zoekterm(idbestandswijziging, zoekterm):
    sql = "insert into " + schema + ".bestandswijziging_zoekterm (idbestandswijziging, zoekterm) values (" + str(
        idbestandswijziging) + ", '" + zoekterm + "')"
    try:
        cursor = db_postgresql.get_connection().cursor()
        cursor.execute(sql)
        db_postgresql.get_connection().commit()
    except Exception as e:
        logging.exception(e)
