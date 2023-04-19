import logging
import os
from datetime import datetime
from multiprocessing import Process

import psutil as psutil
from peewee import *

from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, \
    ManualChecking, pg_db_schema, TempDiffTextAnalysis
from src.repo_extractor.commitextractor import extract_repository
from src.utils import configurator
from src.utils.read_diff import ReadDiff, Language

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))


def initialize():
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        encoding='utf-8')


def create_tables():
    pg_db.create_tables(
        [GhSearchSelection, Selectie, Project, CommitInfo, BestandsWijziging, ManualChecking, TempDiffTextAnalysis],
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
                                   type_of_diff, author_id, project_name, commitdatumtijd,
                                   connection: PostgresqlDatabase):
    sql = "select count(*) from {sch}.tempdifftextanalysis as tdta " \
          "where tdta.idbestandswijziging = {wijz} and tdta.line_number = {ln} ".format(sch=pg_db_schema,
                                                                                        wijz=bestandswijzigingid,
                                                                                        ln=line_number)
    cursor = connection.execute_sql(sql)
    res = cursor.fetchone()
    if res[0] > 0:
        return

    lt = line_text.replace("'", "\"")  # een ' in een string geeft problemen met de sql 'insert
    lt = lt.replace("%", "%%")  # blijkbaar heeft een % een speciale betekenis

    sql = "insert into {sch}.tempdifftextanalysis (idbestandswijziging, filename, location, line_number, line_text, " \
          "primitives, type_of_diff, project_name, author_id, commitdatumtijd) " \
          "values ({wijz}, '{fn}', '{loc}', {ln}, '{lt}', '{pr}', {td}, '{pn}', {aid}, '{cdt}');".format(
        sch=pg_db_schema, wijz=bestandswijzigingid, fn=file_name, loc=location, ln=line_number, lt=lt, pr=primitives,
        td=type_of_diff, pn=project_name, aid=author_id, cdt=commitdatumtijd)

    try:
        connection.execute_sql(sql)
    except IndexError as ie:
        print('--->' + str(ie))
        print('--->' + sql)


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


def __analyse_diffs(thread_id, idva_from, idva_to):
    print("cpu nr" + str(psutil.Process().cpu_num()))
    params_for_db = configurator.get_database_configuration()
    read_diff = ReadDiff(language=Language.ELIXIR)
    sql = "select bw.id, bw.idcommit, bw.locatie, bw.filename, bw.difftext, ci.author_id, pr.naam,ci.commitdatumtijd " \
          "from {sch}.bestandswijziging as bw " \
          "join {sch}.commitinfo as ci on bw.idcommit = ci.id " \
          "join {sch}.project as pr on ci.idproject = pr.id " \
          "where bw.difftext is not null and bw.extensie <> '.md' and bw.id >= {idva_from} and bw.id < {idva_to} " \
          "order by bw.id;".format(sch=pg_db_schema, idva_from=idva_from, idva_to=idva_to)

    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    cursor = connection.execute_sql(sql)
    counter = 1
    for (bestandswijziging_id, id_commit, locatie, filename, diff_text, author_id, pr_name,
         commitdatumtijd) in cursor.fetchall():
        print("thread id: " + str(thread_id))
        print("counter: " + str(counter))
        print("id: " + str(bestandswijziging_id))
        print("filename: " + filename)
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)
        if len(new_lines) > 0:
            print("new lines: " + str(len(new_lines)))
            print(new_lines)
            for (lijnnummer, tekst, primitives) in new_lines:
                __save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                               __list_to_string(primitives), 1, author_id, pr_name, commitdatumtijd,
                                               connection)
        else:
            print("new lines: 0")
        if len(old_lines) > 0:
            print("old lines: " + str(len(old_lines)))
            print(old_lines)
            for (lijnnummer, tekst, primitives) in old_lines:
                __save_temp_diff_text_analysis(bestandswijziging_id, filename, locatie, lijnnummer, tekst,
                                               __list_to_string(primitives), -1, author_id, pr_name, commitdatumtijd,
                                               connection)
        else:
            print("old lines: 0")
        print("--------------------")
        counter += 1
    connection.close()


if __name__ == '__main__':
    try:
        print(psutil.cpu_count())
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        create_tables()
        # GhSearchSampleRequester.get_sample('Elixir')
        # process_repos('Elixir')
        # fetch_authors_per_commit()
        for z in range(0, 100):
            print("run: " + str(z))
            nr_of_commits = BestandsWijziging.select(fn.MAX(BestandsWijziging.id)).scalar()
            result = TempDiffTextAnalysis.select(fn.MAX(TempDiffTextAnalysis.idbestandswijziging)).scalar()
            if result is None:
                result = 0
            if result >= nr_of_commits:
                break

            processes = []
            step = 1000
            c = 0
            for i in range(0, 32):
                t = Process(target=__analyse_diffs, args=(c, result, result + step))
                processes.append(t)
                result += step
                c += 1

            for p in processes:
                p.start()
                p.name = "Thread " + str(p.ident)

            for p in processes:
                p.join()

        logging.info('Finished at:' + str(datetime.now()))
    except Exception as e:
        logging.error('Crashed at:' + str(datetime.now()))
        logging.exception(e)
