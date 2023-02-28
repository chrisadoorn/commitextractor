import logging
from datetime import datetime
from pydriller import Repository
from src import db_postgresql

global db_connectie

# pip install package pydriller
# pip install package mysql-connector-python


def extract_repository(projectname):
    start = datetime.now()
    logging.info('start verwerking ' + projectname + str(start))

    new_id = 0
    val = (projectname, 'Java', new_id)
    project_id = db_postgresql.insert_project(val)
    logging.info("project " + projectname + " inserted with id: " + str(project_id))

    full_repository = Repository(projectname)
    commit_teller = 0
    for commit in full_repository.traverse_commits():
        commit_teller = commit_teller + 1

        commitcursor = db_connectie.cursor()
        commit_datetime = commit.committer_date
        commitMySqlFormat = commit_datetime.strftime("%Y-%m-%d")
        commit_remark = commit.msg  # limit the comment commit.msg[:200]
        sql = "INSERT INTO test.commit(commitdatumtijd, hashvalue, username, emailaddress, remark, idproject) VALUES (%s, %s, %s, %s, %s, %s);"
        val_commit = (
            commitMySqlFormat, commit.hash, commit.author.name, commit.author.email, commit_remark, project_id)
        commitcursor.execute(sql, val_commit)
        commitId = commitcursor.lastrowid
        print('commit: ' + str(commit_teller))

        for file in commit.modified_files:
            # print(file.filename, ' has changed')
            # if not (file.filename.endswith('.zip') or file.filename.endswith('.eot') or file.filename.endswith(
            #       '.woff') or file.filename.endswith('interface.saveScore.loadScore.txt')):
            if file.filename.endswith('.java') or (
                    file.filename == 'pom.xml' and file.new_path == '' and file.old_path == ''):
                # sla op in database
                filecursor = db_connectie.cursor()

                # sql = "INSERT INTO test.bestandswijziging (tekstvooraf, tekstachteraf, difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s, %s, %s)"
                # val = (file.content_before, file.content, file.diff, file.filename, file.new_path, commitId)
                #sql = "INSERT INTO test.bestandswijziging ( tekstachteraf, difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s, %s)"
                #val = (file.content, file.diff, file.filename, file.new_path, commitId)

                sql = "INSERT INTO test.bestandswijziging ( difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s)"
                val = ( file.diff, file.filename, file.new_path, commitId)
                filecursor.execute(sql, val)
                rowId = filecursor.lastrowid
                db_connectie.commit()

    #          print(filecursor.rowcount, "record inserted with id: " + str(rowId))

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
    db_connectie = db_postgresql.open_connection()

    # projectname = db_postgresql.get_next_project('', verwerking_status)
    # while projectname:
    # projectname = 'https://github.com/apache/nifi'
    # projectname = '/git/java/nifi'

    # we gebruiken een inner try voor het verwerken van een enkel project.
    # Als dit foutgaat, dan kan dit aan het project liggen.
    # We stoppen dan met dit project, en starten een volgend project
    try:
        verwerking_status = 'mislukt'
        # extract_repository(projectname)
        verwerking_status = 'verwerkt'
    # continue processing next project
    except Exception as e_inner:
        logging.error('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
        logging.exception(e_inner)


    # projectname = db_postgresql.get_next_project(projectname, verwerking_status)

    logging.info('Starting extracting in new process with id: ' + process_identifier)
    # extract_repository('https://github.com/ishepard/pydriller')
    # extract_repository('/git/java/nifi')

