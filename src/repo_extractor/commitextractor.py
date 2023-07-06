import logging
import os
from peewee import PostgresqlDatabase
from datetime import datetime

from pydriller import Repository, ModifiedFile
from src.repo_extractor import hashing
from src.utils import configurator, db_postgresql

PROCESSTAP = 'extractie'
STATUS_MISLUKT = 'mislukt'
STATUS_VERWERKT = 'verwerkt'

# configurtion options
extensions = configurator.get_extensions()
files = configurator.get_files()
save_code_before = configurator.get_module_configurationitem_boolean(module='repo_extractor', entry='save_before')

PeeWeeConnectionPool = {}

INSERT_COMMITS_SQL = "insert into {schema}.commitinfo (idproject, commitdatumtijd, " \
                     "hashvalue, username, emailaddress, remark) " \
                     "values ({idproject}, '{commitdatumtijd}', " \
                     "'{hashvalue}', '{username}', '{emailaddress}', {remark}) returning id;"

INSERT_FILES_SQL = "insert into {schema}.bestandswijziging " \
                   "(idcommit, filename, locatie, extensie, difftext, " \
                   "tekstvooraf,tekstachteraf) " \
                   "values ({idcommit}, '{filename}', '{locatie}', '{extensie}', {difftext}," \
                   "{tekstvooraf}, {tekstachteraf} ) " \
                   "returning id;"

schema = ''


def __extract_repository(process_identifier: str, projectlocation: str, project_id: int) -> None:
    """
    Process a project by using PyDriller.
    PyDriller downloads the project, and returns a list of all its commits. Each commit contains a list of its filechanges.
    This function loops through those and stores the information.
    :param projectlocation: The location from where you are downloading the project
                        If this is a local or network drive, the project will not be downloaded, but processed in place.
    :param project_id: The database id of the project
    """
    connection = __get_connection_from_pool(process_identifier)

    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectlocation + str(start))
    print('start verwerking (' + str(project_id) + '):  ' + projectlocation + str(start))
    full_repository = Repository(projectlocation)
    for commit in full_repository.traverse_commits():
        try:

            remark = __opkuizen_speciale_tekens(commit.msg, False)
            sql = INSERT_COMMITS_SQL.format(schema=schema, idproject=project_id, commitdatumtijd=commit.committer_date,
                                            hashvalue=commit.hash, username=hashing.make_hash(commit.author.name),
                                            emailaddress=hashing.make_hash(commit.author.email), remark=remark)
            c = connection.execute_sql(sql)
            nw_pk = c.fetchone()
            for file in commit.modified_files:
                __save_bestandswijziging(connection, schema, file, nw_pk[0])
        except (UnicodeDecodeError, ValueError, TypeError) as e_inner:
            logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectlocation + str(eind))
    print('einde verwerking ' + projectlocation + str(eind))
    duur = eind - start
    logging.info('verwerking ' + projectlocation + ' duurde ' + str(duur))


def __save_bestandswijziging(connection: PostgresqlDatabase, schema_in: str, file: ModifiedFile,
                             commit_id: int) -> None:
    """
    Checks if a bestandswijziging is of wanted in further analysis
    If so saves it into the database.
    :param file: PyDriller object: ModifiedFile
    :param commit_id: database id of commitinfo record
    """
    (do_safe, extension) = __file_selector(file)
    if do_safe:
        # sla op in database
        try:
            tekstvooraf = __opkuizen_speciale_tekens(file.content_before, False) if save_code_before else 'null'
            diff_text = __opkuizen_speciale_tekens(file.diff, True)
            tekstachteraf = __opkuizen_speciale_tekens(file.content, False)
            sql = INSERT_FILES_SQL.format(schema=schema_in, idcommit=commit_id, filename=file.filename,
                                          locatie=file.new_path, extensie=extension, difftext=diff_text,
                                          tekstvooraf=tekstvooraf, tekstachteraf=tekstachteraf)
            connection.execute_sql(sql)
        except (UnicodeDecodeError, ValueError, TypeError) as e_inner:
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
            logging.info('start verwerking (' + str(projectid) + '):  ' + projectnaam)
            # We gebruiken een inner try voor het verwerken van een enkel project.
            # Als dit foutgaat, dan kan dit aan het project liggen.
            # We stoppen dan met dit project, en starten een volgend project
            try:
                __extract_repository(process_identifier, projectnaam, projectid)
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


def __opkuizen_speciale_tekens(tekst, not_null):
    """
    Speciale tekens toevoegen aan een string voor gebruik in een PSQL statement
    """
    if tekst is None:
        if not_null:
            return "''"
        return 'null'
    try:
        tekst = tekst.decode()
    except (UnicodeDecodeError, AttributeError):
        pass

    return "'" + tekst.replace("'", "''").replace("%", "%%") + "'"


def __get_connection_from_pool(process_identifier):
    if process_identifier in PeeWeeConnectionPool:
        connection = PeeWeeConnectionPool[process_identifier]
    else:
        params_for_db = configurator.get_database_configuration()
        global schema
        schema = params_for_db.get('schema')
        connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'),
                                        password=params_for_db.get('password'), host=params_for_db.get('host'),
                                        port=params_for_db.get('port'))
        PeeWeeConnectionPool[process_identifier] = connection
    return connection
