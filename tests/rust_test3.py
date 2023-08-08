#logging toevoegen
import logging

from src.models.analyzed_data_models import BestandsWijzigingInfo, BestandsWijzigingZoekterm, , get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from datetime import datetime

#laten lopen util tools voor opkuisen use statements

#laten lopen zoekengine

#aanpassen fulltext

#laten lopen util tools voor opkuisen use statements

#laten lopen parser

#zien of keywoord erin voorkomt, zoniet falsepositive aanzetten

def parse_fulltext_by_project(projectname, project_id):
    start = datetime.now()
    global read_diff
    #logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))
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

            print("full_text " + full_text)

            # kuis de full text op
            #cleanedFullText = cleanUpText(fulltext)


            """
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
            """