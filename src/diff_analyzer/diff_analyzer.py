import logging

from datetime import datetime

import peewee

from src.models.extracted_data_models import BestandsWijziging, CommitInfo
from src.utils import db_postgresql
from src.models.analyzed_data_models import pg_db, pg_db_schema, BestandsWijzigingInfo, BestandsWijzigingZoekterm
from src.utils.read_diff import ReadDiff, Language

global db_connectie


def analyze_by_project(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))

    # haal voor deze commit de lijst bestandswijzig id's op.
    commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project_id)
    for commitInfo in commitinfo_lijst:

        bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(BestandsWijziging.idcommit == commitInfo.id)
        for bestandswijziging in bestandswijzigingen_lijst:

            # haal de gevonden zoektermen voor deze diff op
            lijst = BestandsWijzigingZoekterm.select().where(BestandsWijzigingZoekterm.idbestandswijziging == bestandswijziging.id)
            if len(lijst) == 0:
                # geen zoekterm, dan door naar de volgende
                continue

            # haal zoektermen uit de lijst
            zoektermlijst = []
            for item in lijst:
                zoektermlijst.append(item.zoekterm)

            # haal de diff op
            difftekst_houder = BestandsWijziging.select(BestandsWijziging.difftext).where(BestandsWijziging.id == bestandswijziging.id)

            # doorzoek de diff op de eerder gevonden zoektermen
            read_diff = ReadDiff(language=Language.JAVA, zoeklijst=zoektermlijst)
            (new_lines, old_lines) = read_diff.read_diff_text(difftekst_houder.difftext)

            # sla gevonden resultaten op per bestandswijziging
            bestands_wijziging_info = BestandsWijzigingInfo()
            bestands_wijziging_info.id = bestandswijziging.id
            bestands_wijziging_info.regels_nieuw = len(new_lines)
            bestands_wijziging_info.regels_oud = len(old_lines)
            bestands_wijziging_info.save(force_insert=True)

            # sla gevonden resultaten op per zoekterm in bestandswijziging








    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


def analyze(process_identifier):
    global db_connectie
    oude_processtap = 'extractie'
    nieuwe_processtap = 'zoekterm_controleren'

    try:
        db_connectie = db_postgresql.open_connection()
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
