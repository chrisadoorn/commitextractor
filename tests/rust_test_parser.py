#test file voor parser

import logging

from src.models.analyzed_data_models import get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection
from src.Rust.utils import parseText
from src.models.selection_models import Project

open_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase

# haal voor deze commit de lijst bestandswijziging id's op.
project_lijst = Project.select(Project.id)
for project in project_lijst:
    if project.id < 500:
        commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project.id)
        for commitInfo in commitinfo_lijst:
            bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(
                BestandsWijziging.idcommit == commitInfo.id)

            for bestandswijziging in bestandswijzigingen_lijst:

                # haal de gevonden zoektermen voor deze bestandswijziging op
                bwz_lijst = get_voor_bestandswijziging(bestandswijziging.id)

                # geen zoekterm, dan door naar de volgende
                if len(bwz_lijst) == 0:
                    continue

                """print("project.id " + str(project.id))
                print("commitInfo.id " + str(commitInfo.id))
                print("bestandswijziging.id " + str(bestandswijziging.id))
                print("len(bwz_lijst) " + str(len(bwz_lijst)))
                """
                # haal zoektermen uit de lijst
                zoektermlijst = []
                for (bwz_id, idbestandswijziging, zoekterm, falsepositive, afkeurreden, aantalgevonden_oud, aantalgevonden_nieuw) in bwz_lijst:
                    zoektermlijst.append(zoekterm)
                #print(" " + str(zoektermlijst))

                # haal de full text op
                (tekst_achteraf,) = (BestandsWijziging.select(BestandsWijziging.tekstachteraf).where(
                    BestandsWijziging.id == bestandswijziging.id))
                # kuis de full text op
                fulltext = parseText(tekst_achteraf.tekstachteraf)
                #print("fulltext1 " + fulltext)

                # per zoekterm zien of deze nog voorkomt
                try:
                    for zoekterm in zoektermlijst:
                        zoekterm = zoekterm.replace("%)", "")
                        if zoekterm not in fulltext:
                            #print("fulltext " + fulltext)
                            false_positive = 'True'
                            afkeur_reden = 'parser'
                            print ("zoekterm " + zoekterm + " id " + str(bwz_id) + " idbestandswijziging " + str(idbestandswijziging) + " afkeur_reden " + afkeur_reden + " false_positive " + false_positive)
                            if (zoekterm in ('channel::','sync_channel(%)','sync_channel::','.send(%)','.recv()')) and 'mpsc::' not in fulltext:
                                    false_positive = 'True'
                                    afkeur_reden = 'package'
                            #print ("zoekterm " + zoekterm + " id " + str(bwz_id) + " idbestandswijziging " + str(idbestandswijziging) + " afkeur_reden " + afkeur_reden + " false_positive " + false_positive)
                            #print("PACKAGE IS VERKEERD")
                        else:
                            false_positive = 'False'
                            afkeur_reden = ''
                except InvalidFullText as e:
                    logging.error(f'parseexception: {str(e)}')
                    continue
