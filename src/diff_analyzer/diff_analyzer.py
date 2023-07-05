import logging
from datetime import datetime

from src.models.analyzed_data_models import BestandsWijzigingInfo, BestandsWijzigingZoekterm, delete_regelnummer_by_key, \
    insert_regelnummers_by_key, get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from src.utils import db_postgresql, configurator
from src.utils.read_diff import ReadDiffElixir, ReadDiffJava, ReadDiffRust, _ReadDiff

read_diff = None


def __get_read_diff() -> _ReadDiff:
    global read_diff
    if read_diff is None:
        language = configurator.get_main_language()[0]
        read_diff = ReadDiffElixir() if language.upper() == 'ELIXIR' else (
            ReadDiffJava() if language == 'JAVA' else ReadDiffRust())
    return read_diff


def __update_regelnummers(idbestandswijziging: int, zoekterm: str, new_lines: [int], removed_lines: [int]) -> None:
    """
    Om regelnummers te kunnen updaten worden deze verwijderd, en vervolgens opnieuw opgevoerd.
    :param idbestandswijziging:
    :param new_lines:
    :param removed_lines:
    :param zoekterm:
    """
    delete_regelnummer_by_key(bestandswijzigings_id=idbestandswijziging, zoekterm=zoekterm)
    if len(new_lines) > 0:
        insert_regelnummers_by_key(idbestandswijziging, zoekterm, new_lines, 'nieuw')
    if len(removed_lines) > 0:
        insert_regelnummers_by_key(idbestandswijziging, zoekterm, removed_lines, 'oud')


def analyze_by_project(projectname, project_id):
    start = datetime.now()
    global read_diff
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))
    # haal voor deze commit de lijst bestandswijzig id's op.
    open_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase
    commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project_id)
    for commitInfo in commitinfo_lijst:

        bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(
            BestandsWijziging.idcommit == commitInfo.id)
        for bestandswijziging in bestandswijzigingen_lijst:

            # haal de gevonden zoektermen voor deze diff op
            bwz_lijst = get_voor_bestandswijziging(bestandswijziging.id)
            if len(bwz_lijst) == 0:
                # geen zoekterm, dan door naar de volgende
                continue

            # haal zoektermen uit de lijst
            zoektermlijst = []
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw) in bwz_lijst:
                zoektermlijst.append(zoekterm)

            # haal de diff op
            (difftekst,) = BestandsWijziging.select(BestandsWijziging.difftext).where(
                BestandsWijziging.id == bestandswijziging.id)

            # doorzoek de diff op de eerder gevonden zoektermen

            (new_lines, removed_lines) = __get_read_diff().check_diff_text_no_check_with_removed(difftekst.difftext, zoektermlijst)

            # sla gevonden resultaten op per bestandswijziging
            BestandsWijzigingInfo.insert_or_update(parameter_id=bestandswijziging.id, regels_oud=len(removed_lines),
                                                   regels_nieuw=len(new_lines))

            # sla gevonden resultaten op per zoekterm in bestandswijziging
            # dit overschrijft eerdere versies, dus als de
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw) in bwz_lijst:
                zoekterm = zoekterm
                regelnrs_new = []
                for (regelnr, line, keywords) in new_lines:
                    if zoekterm in keywords:
                        regelnrs_new.append(regelnr)
                regelnrs_old = []
                for (regelnr, line, keywords) in removed_lines:
                    if zoekterm in keywords:
                        regelnrs_old.append(regelnr)

                bestandswijziging_zoekterm = BestandsWijzigingZoekterm()
                bestandswijziging_zoekterm.id = bwz_id
                bestandswijziging_zoekterm.idbestandswijziging = idbestandswijziging
                bestandswijziging_zoekterm.zoekterm = zoekterm
                bestandswijziging_zoekterm.falsepositive = (len(regelnrs_old) == 0 and len(regelnrs_new) == 0)
                bestandswijziging_zoekterm.aantalgevonden_oud = len(regelnrs_old)
                bestandswijziging_zoekterm.aantalgevonden_nieuw = len(regelnrs_new)
                bestandswijziging_zoekterm.save()
                __update_regelnummers(idbestandswijziging, zoekterm, regelnrs_new, regelnrs_old)

    close_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase
    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


def analyze(process_identifier):
    oude_processtap = 'zoekterm_vinden'
    nieuwe_processtap = 'zoekterm_controleren'

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
                analyze_by_project(projectnaam, projectid)
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
