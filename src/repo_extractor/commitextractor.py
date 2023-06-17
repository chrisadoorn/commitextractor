import logging
import os
from datetime import datetime

from pydriller import Repository, ModifiedFile
from src.repo_extractor import hashing
from src.models.extracted_data_models import CommitInfo, BestandsWijziging
from src.utils import configurator, db_postgresql

PROCESSTAP = 'extractie'
STATUS_MISLUKT = 'mislukt'
STATUS_VERWERKT = 'verwerkt'

global db_connectie

# configurtion options
extensions = configurator.get_extensions()
files = configurator.get_files()
save_code_before = configurator.get_module_configurationitem_boolean(module='repo_extractor', entry='save_before')


def __extract_repository(projectlocation: str, project_id: int) -> None:
    """
    Process a project by using PyDriller.
    PyDriller downloads the project, and returns a list of all its commits. Each commit contains a list of its filechanges.
    This function loops through those and stores the information.
   :param projectlocation: The location from where you are downloading the project
                        If this is a local or network drive, the project will not be downloaded, but processed in place.
    :param project_id: The database id of the project
    """
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectlocation + str(start))
    full_repository = Repository(projectlocation)
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
                __save_bestandswijziging(file, commit_info.id)
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectlocation + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectlocation + ' duurde ' + str(duur))
    print(duur)


def __save_bestandswijziging(file: ModifiedFile, commit_id: int) -> None:
    """
    Checks if a bestandswijziging is of wanted in further analysis
    If so saves it into the database.
    :param file: PyDriller object: ModifiedFile
    :param commit_id: database id of commitinfo record
    """
    fs = __file_selector(file)
    if fs[0]:
        # sla op in database
        file_changes = BestandsWijziging()
        file_changes.filename = file.filename
        file_changes.difftext = file.diff
        file_changes.tekstachteraf = file.content
        if save_code_before:
            file_changes.tekstvooraf = file.content_before
        file_changes.idcommit = commit_id
        file_changes.locatie = file.new_path
        file_changes.extensie = fs[1]

        try:
            file_changes.save()
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)


def __file_selector(file: ModifiedFile) -> (bool, str):
    """
    Checks if the file has to be analyzed according to the configuration.
    Returns a tuple ( want to anayze, file name)
    :param file: PyDriller object: ModifiedFile
    :return: tuple, boolean True if file is of a type wanted to be analysed
                    str     The filename
    """
    split_up = os.path.splitext(file.filename)
    # bestand is apart genoemd
    if file.new_path in files:
        try:
            return True, split_up[1]
        except ValueError:
            return False

    # bestand is van gewenst type
    try:
        return split_up[1] in extensions, split_up[1]
    except ValueError:
        return False


# extract_repositories is the starting point for this functionality
# extract repositories while there are repositories to be processed
def extract_repositories(process_identifier: str, oude_processtap: str) -> None:
    global db_connectie
    nieuwe_processtap = PROCESSTAP
    try:
        db_connectie = db_postgresql.open_connection()
        db_postgresql.registreer_processor(process_identifier)

        volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
        rowcount = volgend_project[2]
        while rowcount == 1:
            projectnaam = volgend_project[1]
            projectid = volgend_project[0]
            verwerking_status = STATUS_MISLUKT

            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                __extract_repository(projectnaam, projectid)
                verwerking_status = STATUS_VERWERKT
            # continue processing next project
            except Exception as e_inner:
                logging.error('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
                logging.exception(e_inner)

            # do always
            db_postgresql.registreer_verwerking(projectnaam=projectnaam, processor=process_identifier,
                                                verwerking_status=verwerking_status, projectid=projectid)
            volgend_project = db_postgresql.volgend_project(process_identifier, oude_processtap, nieuwe_processtap)
            rowcount = volgend_project[2]

        # na de loop
        db_postgresql.deregistreer_processor(process_identifier)

    except Exception as e_outer:
        logging.error('Er zijn fouten geconstateerd tijdens het loopen door de projectenlijst. Zie details hieronder')
        logging.exception(e_outer)
