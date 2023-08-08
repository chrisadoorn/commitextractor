# delete comments of the form " ", ' ', //, ///, //! and of the form /* ... */
# logging toevoegen zie repoextractor.py

import pyparsing as pp
import os
import logging
from datetime import datetime #waar gebruiken

from src.models.analyzed_data_models import BestandsWijzigingInfo, BestandsWijzigingZoekterm, delete_regelnummer_by_key, \
    insert_regelnummers_by_key, get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from datetime import datetime
from src.utils import configurator, db_postgresql

class InvalidFullText(Exception):
    """Raised when the diff text is not valid"""
    pass

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


def parse_fulltext_by_project(projectname, project_id):
    start = datetime.now()
    global read_diff
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))
    open_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase

    # haal voor deze commit de lijst bestandswijziging id's op.
    commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project_id)
    for commitInfo in commitinfo_lijst:
        bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(
            BestandsWijziging.idcommit == commitInfo.id)

        for bestandswijziging in bestandswijzigingen_lijst:

            # haal de gevonden zoektermen voor deze bestandswijziging op
            bwz_lijst = get_voor_bestandswijziging(bestandswijziging.id)
            if len(bwz_lijst) == 0:
                # geen zoekterm, dan door naar de volgende
                continue

            # haal zoektermen uit de lijst
            zoektermlijst = []
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw) in bwz_lijst:
                zoektermlijst.append(zoekterm)

            # haal de full text op
            fulltext = BestandsWijziging.select(BestandsWijziging.tekstachteraf).where(
                BestandsWijziging.id == bestandswijziging.id)
            # kuis de full text op
            cleanedFullText = cleanUpText(fulltext)

            # doorzoek de fulltext op de eerder gevonden zoektermen
            # per zoekterm zien of deze nog voorkomt
            try:
                for zoekterm in zoektermlijst:
                    if zoekterm not in cleanedFullText:
                        # vlaggen als false_positive met afkeurreden multiline
            except InvalidFullText as e:
                logging.error('parseexception: ' + str(e))
                continue

            # sla gevonden resultaten op per bestandswijziging
            BestandsWijzigingInfo.insert_or_update(parameter_id=bestandswijziging.id, regels_oud=len(removed_lines),
                                                   regels_nieuw=len(new_lines))

            # sla gevonden resultaten op per zoekterm in bestandswijziging
            # dit overschrijft eerdere versies, dus als de
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw) in bwz_lijst:
                zoekterm = zoekterm
                regelnrs_new = []
                for (regelnr, line, keywords) in new_lines:
                    count = keywords.count(zoekterm)
                    for i in range(count):
                        regelnrs_new.append(regelnr)
                regelnrs_old = []
                for (regelnr, line, keywords) in removed_lines:
                    count = keywords.count(zoekterm)
                    for i in range(count):
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


def parse_fulltext(process_identifier):
    oude_processtap = 'zoekterm_controleren'
    nieuwe_processtap = 'fulltext_controleren'

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
                parse_fulltext_by_project(projectnaam, projectid)
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

def cleanUpText (full_text: str) -> str:
    comment = pp.cppStyleComment + pp.rest_of_line
    comment2 = (comment.suppress().transform_string(full_text))
    comment3 = pp.quoted_string + (comment.suppress().transform_string(comment2))
    return comment3

