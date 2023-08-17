import logging
from src.models.analyzed_data_models import BestandsWijzigingZoekterm, get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from datetime import datetime
from src.utils import db_postgresql
from src.Rust.utils import parseText

class InvalidFullText(Exception):
    """Raised when the full text is not valid"""
    pass

def parse_fulltext_by_project(projectname, project_id):
    start = datetime.now()
    global read_diff, false_positive, afkeur_reden
    logging.info(
        f'start verwerking ({str(project_id)}):  {projectname}{str(start)}'
    )
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

            zoektermlijst = [
                zoekterm
                for bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden in bwz_lijst
            ]
            # haal de full text op
            fulltext = BestandsWijziging.select(BestandsWijziging.tekstachteraf).where(
                BestandsWijziging.id == bestandswijziging.id)
            # kuis de full text op
            fulltext = parseText(fulltext)

            # per zoekterm zien of deze nog voorkomt
            try:
                for zoekterm in zoektermlijst:
                    if zoekterm not in fulltext:
                        false_positive = 'True'
                        afkeur_reden = 'parser'
                    else:
                        false_positive = 'False'
                        afkeur_reden = ''
            except InvalidFullText as e:
                logging.error(f'parseexception: {str(e)}')
                continue

            # sla gevonden resultaten op per zoekterm in bestandswijziging
            for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden) in bwz_lijst:
                zoekterm = zoekterm
                bestandswijziging_zoekterm = BestandsWijzigingZoekterm()
                bestandswijziging_zoekterm.id = bwz_id
                bestandswijziging_zoekterm.idbestandswijziging = idbestandswijziging
                bestandswijziging_zoekterm.afkeurreden = afkeur_reden
                bestandswijziging_zoekterm.zoekterm = zoekterm
                bestandswijziging_zoekterm.falsepositive = false_positive
                bestandswijziging_zoekterm.save()

    close_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase
    eind = datetime.now()
    logging.info(f'einde verwerking {projectname}{str(eind)}')
    print(eind)
    duur = eind - start
    logging.info(f'verwerking {projectname} duurde {str(duur)}')
    print(duur)


def parse_fulltext(process_identifier):
    oude_processtap = 'zoekterm_vinden'
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
        logging.error('Er zijn fouten geconstateerd tijdens het lopen door de projectenlijst. Zie details hieronder')
        logging.exception(e_outer)


