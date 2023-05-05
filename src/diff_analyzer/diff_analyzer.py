import logging

from datetime import datetime

from src.models.extracted_data_models import BestandsWijziging, CommitInfo
from src.utils import db_postgresql, configurator
from src.models.analyzed_data_models import BestandsWijzigingInfo, BestandsWijzigingZoekterm
from src.utils.read_diff import ReadDiff


def analyze_by_project(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))

    # bepaal taal waarvoor gezocht moet worden
    language = configurator.get_main_language()[0]

    # haal voor deze commit de lijst bestandswijzig id's op.
    commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project_id)
    for commitInfo in commitinfo_lijst:

        bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(
            BestandsWijziging.idcommit == commitInfo.id)
        for bestandswijziging in bestandswijzigingen_lijst:

            # haal de gevonden zoektermen voor deze diff op
            bestandswijziging_id = bestandswijziging.id
            bwz_lijst = BestandsWijzigingZoekterm.get_voor_bestandswijziging(bestandswijziging_id)
            if len(bwz_lijst) == 0:
                # geen zoekterm, dan door naar de volgende
                continue

            # haal zoektermen uit de lijst
            zoektermlijst = []
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, regelnummers, aantalgevonden) in bwz_lijst:
                zoektermlijst.append(zoekterm)

            # haal de diff op
            (difftekst,) = BestandsWijziging.select(BestandsWijziging.difftext).where(
                BestandsWijziging.id == bestandswijziging_id)

            # doorzoek de diff op de eerder gevonden zoektermen
            read_diff = ReadDiff(language=language, zoeklijst=zoektermlijst)
            (new_lines, old_lines) = read_diff.read_diff_text(difftekst.difftext)

            # sla gevonden resultaten op per bestandswijziging
            BestandsWijzigingInfo.insert_or_update(parameter_id=bestandswijziging_id, regels_oud=len(old_lines),
                                                   regels_nieuw=len(new_lines))

            # sla gevonden resultaten op per zoekterm in bestandswijziging
            # dit overschrijft eerdere versies, dus als de
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, regelnummers, aantalgevonden) in bwz_lijst:
                zoekterm = zoekterm
                regelnrs = []
                for (regelnr, line, keywords) in new_lines:
                    if zoekterm in keywords:
                        regelnrs.append(regelnr)

                bestandswijziging_zoekterm = BestandsWijzigingZoekterm()
                bestandswijziging_zoekterm.id = bwz_id
                bestandswijziging_zoekterm.idbestandswijziging = idbestandswijziging
                bestandswijziging_zoekterm.zoekterm = zoekterm
                bestandswijziging_zoekterm.falsepositive = (len(regelnrs) == 0)
                bestandswijziging_zoekterm.regelnummers = regelnrs
                bestandswijziging_zoekterm.aantalgevonden = len(regelnrs)
                bestandswijziging_zoekterm.save()

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
