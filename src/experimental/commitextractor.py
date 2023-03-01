import logging
from datetime import datetime
from pydriller import Repository
from src import db_postgresql
from src.experimental.models import CommitInformation


def extract_repository(projectname,project_id):
    start = datetime.now()
    logging.info('start verwerking ' + projectname + str(start))
    full_repository = Repository(projectname)
    commit_teller = 0
    for commit in full_repository.traverse_commits():
        commit_teller = commit_teller + 1
        db_commit = CommitInformation()
        db_commit.remark = commit.msg
        db_commit.commit_date_time = commit.committer_date
        db_commit.email_address = commit.author.email
        db_commit.hash_value = commit.hash
        db_commit.id_project = project_id
        db_commit.username = commit.author.name
        db_commit.save()

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
                # sql = "INSERT INTO test.bestandswijziging ( tekstachteraf, difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s, %s)"
                # val = (file.content, file.diff, file.filename, file.new_path, commitId)

                sql = "INSERT INTO test.bestandswijziging ( difftext, filename, locatie, idcommit) VALUES (%s, %s, %s, %s)"
                val = (file.diff, file.filename, file.new_path, commitId)
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
