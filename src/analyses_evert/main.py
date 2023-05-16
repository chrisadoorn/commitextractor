import logging
import math
import os
from datetime import datetime
from multiprocessing import Process

import psutil as psutil
from peewee import *

from src.analyses_evert.read_diff_evert import ReadDiffEvert
from src.models.models import GhSearchSelection, pg_db, CommitInfo, BestandsWijziging, Selectie, Project, pg_db_schema, \
    TempDiffTextAnalysis
from src.repo_extractor.commitextractor import extract_repository
from src.utils import configurator
from src.utils.read_diff import ReadDiff

dt = datetime.now()
filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'main.' + str(dt) + '.log'))


def initialize():
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        encoding='utf-8')


def create_tables():
    pg_db.create_tables(
        [TempDiffTextAnalysis],
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
    read_diff = ReadDiff(language="ELIXIR")
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
    ELIXIR_MC_INDICATOR = ["spawn", "spawn_link", "spawn_monitor", "send", "self", "receive", "flush" "Agent", "GenServer",
                           "Node", "Process", "Supervisor", "Task"]
    for (bestandswijziging_id, id_commit, locatie, filename, diff_text, author_id, pr_name,
         commitdatumtijd) in cursor.fetchall():
        print("thread id: " + str(thread_id))
        print("counter: " + str(counter))
        print("id: " + str(bestandswijziging_id))
        print("filename: " + filename)
        (new_lines, old_lines) = read_diff.check_diff_text(diff_text, ELIXIR_MC_INDICATOR)
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


NUMBER_OF_PROCESSES = 32


def analyse_b_wijzigingen(language):
    try:
        print(psutil.cpu_count())
        initialize()
        logging.info('Started at:' + str(datetime.now()))
        create_tables()
        # GhSearchSampleRequester.get_sample('Elixir')
        # process_repos('Elixir')
        # fetch_authors_per_commit()
        for z in range(0, 1):
            print("run: " + str(z))
            hoogste_bw_id = BestandsWijziging.select(fn.MAX(BestandsWijziging.id)).scalar()
            laagste_bw_id = BestandsWijziging.select(fn.MIN(BestandsWijziging.id)).scalar()
            verschil = hoogste_bw_id - laagste_bw_id
            stap_grootte = math.ceil(verschil / NUMBER_OF_PROCESSES)
            processes = []
            step = stap_grootte
            start_id = laagste_bw_id
            c = 0
            for i in range(0, NUMBER_OF_PROCESSES):
                t = Process(target=__analyse_diffs, args=(c, start_id, start_id + step))
                processes.append(t)
                start_id += step
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


def copy_bestands_wijziging():
    # take_sample()
    setattr(CommitInfo._meta, "schema", "test_sample")
    commit_info = CommitInfo.select()  # neem alle projecten van de test_sample schema
    bestandwijziging = []
    setattr(BestandsWijziging._meta, "schema", "prod")
    for ci in commit_info:
        bw = BestandsWijziging.select().where(BestandsWijziging.idcommit == ci.id)
        bestandwijziging.extend(bw)
    setattr(BestandsWijziging._meta, "schema", "test_sample")
    for b in bestandwijziging:
        bw = BestandsWijziging()
        bw.id = b.id
        bw.idcommit = b.idcommit
        bw.locatie = b.locatie
        bw.filename = b.filename
        bw.extensie = b.extensie
        bw.difftext = b.difftext
        bw.tekstachteraf = b.tekstachteraf
        bw.save(force_insert=True)


def copy_commit_info_schema():
    # take_sample()
    setattr(Project._meta, "schema", "test_sample")
    test_sample_schema_projecten = Project.select()  # neem alle projecten van de test_sample schema

    commit_info = []
    setattr(CommitInfo._meta, "schema", "prod")

    for p in test_sample_schema_projecten:
        ci = CommitInfo.select().where(CommitInfo.idproject == p.id)
        commit_info.extend(ci)

    setattr(CommitInfo._meta, "schema", "test_sample")
    for c in commit_info:
        ci = CommitInfo()
        ci.id = c.id
        ci.idproject = c.idproject
        ci.commitdatumtijd = c.commitdatumtijd
        ci.hashvalue = c.hashvalue
        ci.username = c.username
        ci.emailaddress = c.emailaddress
        ci.remark = c.remark
        ci.author_id = c.author_id
        ci.save(force_insert=True)


def take_sample():
    # schema = 'prod'
    setattr(Project._meta, "schema", "prod")
    prod_schema = Project.select().order_by(fn.Random())
    projectsList = []
    for s in prod_schema.limit(100):
        print(s.naam)
        projectsList.append(s)

    # schema = 'test_sample
    setattr(Project._meta, "schema", "test_sample")

    for p in projectsList:
        pr = Project()
        pr.id = p.id
        pr.naam = p.naam
        pr.idselectie = p.idselectie
        pr.main_language = p.main_language
        pr.is_fork = p.is_fork
        pr.license = p.license
        pr.forks = p.forks
        pr.contributors = p.contributors
        pr.project_size = p.project_size
        pr.create_date = p.create_date
        pr.last_commit = p.last_commit
        pr.number_of_languages = p.number_of_languages
        pr.languages = p.languages
        pr.aantal_commits = p.aantal_commits
        pr.save(force_insert=True)


def copy_sample():
    take_sample()
    copy_commit_info_schema()
    copy_bestands_wijziging()


if __name__ == '__main__':
    rdt = ReadDiffEvert()
    print(rdt.find_key_words('Elixir', 'Elixir') == 1)
    print(rdt.find_key_words(' Elixir ', 'Elixir') == 1)
    print(rdt.find_key_words(' Elixira ', 'Elixir') == 0)
    print(rdt.find_key_words(' Elixir a ', 'Elixir') == 1)
    print(rdt.find_key_words(' ElixirE ElixirElixir a Elixir', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! elixi Elixir a ', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! elixi /Elixir a ', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! elixi //Elixir a ', 'Elixir') == 0)
    print(rdt.find_key_words('s b ! elixie //Elixir a ', 'Elixir') ==0)
    print(rdt.find_key_words('s b ! Elixir //Elixir a ', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! Elixir /*Elixir a ', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! /*Elixir Elixir a ', 'Elixir') == 0)
    print(rdt.find_key_words('s b ! Elixir Elixir a */', '') == 0)
    print(rdt.find_key_words('s b ! Elixir Elixir a */', 'Elixir') == 0)

    print(rdt.find_key_words('s b ! Elixir Elixir a */Elixir', 'Elixir') == 1)
    print(rdt.find_key_words('s b ! Elixir Elixir a "*"/', 'Elixir') == 2)
    print(rdt.find_key_words('s b ! Elixir Elixir a *"/"', 'Elixir') == 2)

    print(rdt.find_key_words('s b ! "Elixir Elixir a */E"lixir', 'Elixir') == 0)
    print(rdt.find_key_words('s b ! "Elixir Elixir a *"/Elixir', 'Elixir') == 1)