import logging
from datetime import datetime

from pydriller import Repository
import hashing
from src.models.extracted_data_models import CommitInfo, BestandsWijziging
from src.utils import configurator, db_postgresql

global db_connectie


# pip install package pydriller
# pip install package mysql-connector-python


def extract_repository(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))

    full_repository = Repository('https://github.com/' + projectname)
    for commit in full_repository.traverse_commits():

        commit_info = CommitInfo()
        commit_info.idproject = project_id
        commit_info.commitdatumtijd = commit.committer_date
        commit_info.hashvalue = commit.hash
        commit_info.username = hashing.make_hash(commit.author.name)
        commit_info.emailaddress = hashing.make_hash(commit.author.email)
        commit_info.remark = commit.msg

        try:
            commit_info.save()
            for file in commit.modified_files:
                save_bestandswijziging(file, commit_info.id)
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


def save_bestandswijziging(file, commit_id):
    extensions = configurator.get_extensions()

    for x in range(len(extensions)):
        if file.filename.endswith(extensions[x]):
            # sla op in database
            file_changes = BestandsWijziging()
            file_changes.filename = file.filename
            file_changes.difftext = file.diff
            file_changes.tekstachteraf = file.content
            file_changes.idcommit = commit_id
            file_changes.locatie = file.new_path
            try:
                file_changes.save()
            except UnicodeDecodeError as e_inner:
                logging.exception(e_inner)
            except ValueError as e_inner:
                logging.exception(e_inner)


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
