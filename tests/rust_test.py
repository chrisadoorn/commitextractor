import logging
import re
from datetime import datetime

from src.models.analyzed_data_models import BestandsWijzigingInfo, get_voor_bestandswijziging
from src.models.extracted_data_models import BestandsWijziging, CommitInfo, open_connection, close_connection
from src.utils.read_diff import ReadDiffRust, InvalidDiffText

def analyze_by_project(projectname, project_id):
    start = datetime.now()
    global read_diff
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))
    # haal voor deze commit de lijst bestandswijzig id's op.
    open_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase
    commitinfo_lijst = CommitInfo.select(CommitInfo.id).where(CommitInfo.idproject == project_id)
    for commitInfo in commitinfo_lijst:
        # haal alle bestandswijzigingen op
        bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id).where(BestandsWijziging.idcommit == commitInfo.id)
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

            # haal de diff op
            (difftekst,) = BestandsWijziging.select(BestandsWijziging.difftext).where(
                BestandsWijziging.id == bestandswijziging.id)

            # doorzoek de diff op de eerder gevonden zoektermen

            try:
                (new_lines, removed_lines) = ReadDiffRust().check_diff_text(difftekst.difftext, zoektermlijst)
            except InvalidDiffText as e:
                logging.error('parseexception: ' + str(e))
                continue
            print("new_lines" + str(new_lines))
            print("removed_lines" + str(removed_lines))

            # sla gevonden resultaten op per bestandswijziging
            #BestandsWijzigingInfo.insert_or_update(parameter_id=bestandswijziging.id, regels_oud=len(removed_lines), regels_nieuw=len(new_lines))

            """
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
                """
    close_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase

@staticmethod
def read_diff_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk

def print_line(file_path: str):
    content = ""
    inside_braces = False
    module_with_braces = None

    with open(file_path, 'r') as file:
        for line in file:
            if inside_braces:
                print("inside_braces ")
                if '};' not in line:
                if '};' in line:
                    end_index = line.index('};')
                    modules_inside_braces = line[:end_index].split(',')
                    for module in modules_inside_braces:
                        if line[0] == '+':
                            content += f"+use {module_with_braces}::{module.lstrip().rstrip()};\n"
                        elif line[0] == '-':
                            content += f"-use {module_with_braces}::{module.lstrip().rstrip()};\n"
                        else:
                            content += f"use {module_with_braces}::{module.lstrip().rstrip()};\n"
                    inside_braces = False
                else:
                    continue
            elif 'use std' in line and '::{' in line:
                print("Use IN LINE ")
                start_index = line.index('use') + 4
                end_index = line.index('::{')
                module_with_braces = line[start_index:end_index].strip()
                print("module_with_braces " + module_with_braces)
                inside_braces = True
                content2=""
            else:
                content += line

    content = re.sub(r'\n\s*\n', '\n', content)
    return content

if __name__ == '__main__':
    keywords = ["std::thread", "std::sync","std::os::raw::Thread"]
    diff_text = read_diff_file(filepath='./data/read_diff_rust.txt')
    file_path = "./data/read_diff_rust.txt"
    print(print_line(file_path))
#    (new_lines, old_lines) = ReadDiffRust().check_diff_text(print_line(file_path), keywords)
#    print("new_lines" + str(new_lines))
#    print("old_lines" + str(old_lines))

    #analyze_by_project('ciantic/virtualdesktopaccessor',58)
