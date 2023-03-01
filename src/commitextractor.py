import logging
from datetime import datetime
from pydriller import Repository
from src import db_postgresql

global db_connectie


# pip install package pydriller
# pip install package mysql-connector-python


def extract_repository(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))

    full_repository = Repository('https://github.com/' + projectname)
    commit_teller = 0
    for commit in full_repository.traverse_commits():
        commit_teller = commit_teller + 1

        commitcursor = db_connectie.cursor()
        commit_datetime = commit.committer_date
        commit_my_sql_format = commit_datetime.strftime("%Y-%m-%d")
        commit_remark = commit.msg  # to limit the comment commit.msg[:200]
        sql = "INSERT INTO test.commit(commitdatumtijd, hashvalue, username, emailaddress, remark, idproject)" \
              " VALUES (%s, %s, %s, %s, %s, %s);"
        val_commit = (
            commit_my_sql_format, commit.hash, commit.author.name, commit.author.email, commit_remark, project_id)
        commitcursor.execute(sql, val_commit)
        commit_id = commitcursor.lastrowid
        print('commit: ' + str(commit_teller))

        for file in commit.modified_files:
            # print(file.filename, ' has changed')
            # if not (file.filename.endswith('.zip') or file.filename.endswith('.eot') or file.filename.endswith(
            #       '.woff') or file.filename.endswith('interface.saveScore.loadScore.txt')):
            if file.filename.endswith('.java') or (
                    file.filename == 'pom.xml' and file.new_path == '' and file.old_path == ''):
                # sla op in database
                filecursor = db_connectie.cursor()

                # sql = "INSERT INTO test.bestandswijziging (tekstvooraf, tekstachteraf, difftext, filename, locatie,
                # idcommit) VALUES (%s, %s, %s, %s, %s, %s)"
                # val = (file.content_before, file.content, file.diff, file.filename, file.new_path, commit_id)
                # sql = "INSERT INTO test.bestandswijziging ( tekstachteraf, difftext, filename, locatie, idcommit)
                # VALUES (%s, %s, %s, %s, %s)"
                # val = (file.content, file.diff, file.filename, file.new_path, commit_id)

                sql = "INSERT INTO test.bestandswijziging ( difftext, filename, locatie, idcommit) " \
                      "VALUES (%s, %s, %s, %s)"
                val = (file.diff, file.filename, file.new_path, commit_id)
                filecursor.execute(sql, val)
                db_connectie.commit()

    print("aantal commits : " + str(commit_teller))

    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


# extract_repositories is the starting point for this functionality
# extract repositories while there are repositories to be processed
def extract_repositories(process_identifier):
    global db_connectie

    try:
        db_connectie = db_postgresql.open_connection()
        db_postgresql.registreer_processor(process_identifier)

        volgend_project = db_postgresql.volgend_project(process_identifier)
        rowcount = volgend_project[2]
        while rowcount == 1:
            projectnaam = volgend_project[1]
            projectid = volgend_project[0]
            verwerking_status = 'mislukt'

            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                extract_repository(projectnaam, projectid)
                verwerking_status = 'verwerkt'
            # continue processing next project
            except Exception as e_inner:
                logging.error('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
                logging.exception(e_inner)

            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid)
            volgend_project = db_postgresql.volgend_project(process_identifier)
            rowcount = volgend_project[2]

        # na de loop
        db_postgresql.deregistreer_processor(process_identifier)

    except Exception as e_outer:
        logging.error('Er zijn fouten geconstateerd tijdens het loopen door de projectenlijst. Zie details hieronder')
        logging.exception(e_outer)
