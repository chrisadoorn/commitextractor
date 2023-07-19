import logging
from datetime import datetime

from pydriller import Repository

from src.repo_extractor import hashing
from src.utils import configurator, db_postgresql

PROCESSTAP = 'extractie'
STATUS_MISLUKT = 'mislukt'
STATUS_VERWERKT = 'verwerkt'

# configurtion options
extensions = configurator.get_extensions()
files = configurator.get_files()
save_code_before = configurator.get_module_configurationitem_boolean(module='repo_extractor', entry='save_before')

connection = None

INSERT_COMMITS_SQL = "insert into {schema}.commitinfo_temp (idproject, commitdatumtijd, " \
                     "hashvalue, username, emailaddress, remark) " \
                     "values ({idproject}, '{commitdatumtijd}', " \
                     "'{hashvalue}', '{username}', '{emailaddress}') returning id;"


import os
from peewee import PostgresqlDatabase
schema = ''

def __extract_repository(projectlocation: str, project_id: int) -> None:
    """
    Process a project by using PyDriller.
    PyDriller downloads the project, and returns a list of all its commits. Each commit contains a list of its filechanges.
    This function loops through those and stores the information.
    :param projectlocation: The location from where you are downloading the project
                        If this is a local or network drive, the project will not be downloaded, but processed in place.
    :param project_id: The database id of the project
    """
    global connection

    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectlocation + str(start))
    print('start verwerking (' + str(project_id) + '):  ' + projectlocation + str(start))
    full_repository = Repository(projectlocation)
    for commit in full_repository.traverse_commits():
        try:

            sql = INSERT_COMMITS_SQL.format(schema=schema, idproject=project_id, commitdatumtijd=commit.committer_date,
                                            hashvalue=commit.hash, username=hashing.make_hash(commit.author.name),
                                            emailaddress=hashing.make_hash(commit.author.email))
            c = connection.execute_sql(sql)
            c.fetchone()

        except (UnicodeDecodeError, ValueError, TypeError) as e_inner:
            logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectlocation + str(eind))
    print('einde verwerking ' + projectlocation + str(eind))
    duur = eind - start
    logging.info('verwerking ' + projectlocation + ' duurde ' + str(duur))


# extract_repositories is the starting point for this functionality
# extract repositories while there are repositories to be processed
def extract_repositories(process_identifier: str, oude_processtap: str) -> None:
    nieuwe_processtap = PROCESSTAP
    try:
        __set_connection()
        db_postgresql.open_connection()
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


def __set_connection():
    global connection
    if connection is None:
        params_for_db = configurator.get_database_configuration()
        global schema
        schema = params_for_db.get('schema')
        connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'),
                                        password=params_for_db.get('password'), host=params_for_db.get('host'),
                                        port=params_for_db.get('port'))
    return connection