#test file voor parser
#logging toevoegen
#check op keywords in combi met bib

import logging

from src.models.analyzed_data_models import BestandsWijzigingInfo, BestandsWijzigingZoekterm, , get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from datetime import datetime
from src.Rust.utils import parseText, checkCorrectPackage

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
                    print ("zoekterm " + zoekterm + " id " + bwz_id + " idbestandswijziging " + idbestandswijziging + " afkeur_reden " + afkeur_reden + "false_positive" + false_positive)
                    if (zoekterm in ('channel::','sync_channel(%)','sync_channel::','.send(%)','.recv()')) and 'mpsc::' not in fulltext:
                            false_positive = 'True'
                            afkeur_reden = 'package'
                else:
                    false_positive = 'False'
                    afkeur_reden = ''
        except InvalidFullText as e:
            logging.error(f'parseexception: {str(e)}')
            continue
