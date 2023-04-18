import logging
import os
from datetime import datetime
from peewee import *
from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, \
    ManualChecking, pg_db_schema, TempDiffTextAnalysis
from src.repo_extractor.commitextractor import extract_repository
from src.requester.api_requester import fetch_authors_per_commit
from src.utils.read_diff import ReadDiff, Language

dt = datetime.now()
filename = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '..', '..', 'log', 'main.' + str(dt) + '.log'))


def initialize():
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


def create_tables():
    pg_db.create_tables([GhSearchSelection, Selectie, Project, CommitInfo, BestandsWijziging, ManualChecking,
                         TempDiffTextAnalysis],
                        safe=True)


def process_repos(subproject):
    ghs = GhSearchSelection.select().where(GhSearchSelection.sub_study == subproject,
                                           GhSearchSelection.meta_import_started_at.is_null(),
                                           GhSearchSelection.meta_import_ready_at.is_null())

    selection = Selectie()
    selection.language = subproject
    selection.save()

    for t in ghs.select():
        project = Project()
        project.naam = t.name
        project.idselectie = selection.id
        project.main_language = t.main_language
        project.is_fork = t.is_fork
        project.license = t.license
        project.forks = t.forks
        project.contributors = t.contributors
        project.project_size = t.size
        project.create_date = t.created_at
        project.last_commit = t.last_commit
        project.number_of_languages = 0
        project.languages = ""
        project.aantal_commits = t.commits
        project.save()

        print(t.name)
        t.meta_import_started_at = datetime.now()

        try:
            extract_repository(t.name, project.id)
            t.selected_for_survey = True
        except Exception as e:
            t.selected_for_survey = False
            print(e)
        t.meta_import_ready_at = datetime.now()
        t.save()


def __save_temp_diff_text_analysis(bestandswijzigingid, file_name, location, line_number, line_text, primitives,
                                   type_of_diff, author_id, project_name, commitdatumtijd):
    if TempDiffTextAnalysis.select().where(TempDiffTextAnalysis.idbestandswijziging == bestandswijzigingid,
                                           TempDiffTextAnalysis.line_number == line_number).exists():
        return

    temp_diff_text_analysis = TempDiffTextAnalysis()
    temp_diff_text_analysis.idbestandswijziging = bestandswijzigingid
    temp_diff_text_analysis.filename = file_name
    temp_diff_text_analysis.location = location
    temp_diff_text_analysis.line_number = line_number
    temp_diff_text_analysis.line_text = line_text
    temp_diff_text_analysis.primitives = primitives
    temp_diff_text_analysis.type_of_diff = type_of_diff
    temp_diff_text_analysis.project_name = project_name
    temp_diff_text_analysis.author_id = author_id
    temp_diff_text_analysis.commitdatumtijd = commitdatumtijd
    temp_diff_text_analysis.save()


def __list_to_string(s):
    str1 = ""
    i = 0
    x = len(s)
    for ele in s:
        if 0 < i < x:
            str1 += ","
        str1 += ele
        i += 1
    return str1


def __analyse_diffs(limit=1000):
    result = TempDiffTextAnalysis.select(fn.MAX(TempDiffTextAnalysis.idbestandswijziging)).scalar()
    if result is None:
        result = 0

    read_diff = ReadDiff(language=Language.ELIXIR)
    sql = "select bw.id, bw.idcommit, bw.locatie, bw.filename, bw.difftext, ci.author_id, pr.naam,ci.commitdatumtijd " \
          "from {sch}.bestandswijziging as bw " \
          "join {sch}.commitinfo as ci on bw.idcommit = ci.id " \
          "join {sch}.project as pr on ci.idproject = pr.id " \
          "where bw.difftext is not null and bw.extensie <> '.md' and bw.id >= {idva} order by bw.id " \
          "limit({li});".format(sch=pg_db_schema, idva=result, li=limit)

    cursor = pg_db.execute_sql(sql)
    counter = 1
    for (bestandswijziging_id, id_commit, locatie, filename, diff_text, author_id, pr_name,
         commitdatumtijd) in cursor.fetchall():
        print("counter: " + str(counter))
        print("id: " + str(bestandswijziging_id))
        print("filename: " + filename)
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)
        if len(new_lines) > 0:
            print("new lines: " + str(len(new_lines)))
            print(new_lines)
            for (lijnnummer, tekst, primitives) in new_lines:
                __save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                               __list_to_string(primitives), 1, author_id, pr_name, commitdatumtijd)
        else:
            print("new lines: 0")
        if len(old_lines) > 0:
            print("old lines: " + str(len(old_lines)))
            print(old_lines)
            for (lijnnummer, tekst, primitives) in old_lines:
                __save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                               __list_to_string(primitives), -1, author_id, pr_name, commitdatumtijd)
        else:
            print("old lines: 0")
        print("--------------------")
        counter += 1


if __name__ == '__main__':
    try:
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        create_tables()
        # GhSearchSampleRequester.get_sample('Elixir')
        # process_repos('Elixir')
        # fetch_authors_per_commit()
        __analyse_diffs(1_000_000)
        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
