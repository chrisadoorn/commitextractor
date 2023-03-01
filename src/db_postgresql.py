import logging

import psycopg2

from src import configurator

global db_conn

DATABASE_INI = '../var/commitextractor.ini'


def _get_connection():
    params = configurator.get_database_configuration()
    v_host = params.get('host')
    conn = psycopg2.connect(host=params.get('host'),
                            port=params.get('port'),
                            user=params.get('user'),
                            password=params.get('password'),
                            database=params.get('database'),
                            options="-c search_path=" + params.get('schema'))
    logging.info('opened a database connection')
    return conn


# known error: if all other connection parameters are correct but the password is incorrect, there is no error detected.
def check_connection():
    # check_connection()
    # helper function for sanity check
    conn = False
    failure = False
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute('select * from selectie where id = 1')
        cursor.close()
    except Exception as e:
        logging.error('Error connecting to database')
        logging.exception(e)
        failure = True
    finally:
        if conn:
            conn.close()

    logging.info('Created connection to database')
    return conn and not failure


def open_connection():
    # open_connection()
    # create a connection and cache this connection
    global db_conn
    db_conn = _get_connection()
    return db_conn


def insert_project(values):
    # insert_project(values)
    # voor testdoeleinden
    sql = 'CALL test.insert_project(%s, %s, %s)'
    projectcursor = db_conn.cursor()
    projectcursor.execute(sql, values)
    resultaattuple = projectcursor.fetchone()
    db_conn.commit()
    projectcursor.close()
    # geef resultaat terug
    return resultaattuple[0]


def get_next_project(projectnaam, processor, verwerking_status):
    logging.info(processor + ' heeft project: ' + projectnaam + ' verwerkt met status: ' + verwerking_status)
    new_id = 0

    if verwerking_status and len(verwerking_status) > 0:
        values = (processor, projectnaam, verwerking_status)
        sql = 'CALL registreer_verwerking(%s, %s, %s)'
        verwerkingcursor = db_conn.cursor()
        verwerkingcursor.execute(sql, values)
        db_conn.commit()
        verwerkingcursor.close()

    values = (processor, projectnaam)
    sql = 'CALL vraag_volgend_project(%s, %s)'
    projectcursor = db_conn.cursor()
    projectcursor.execute(sql, values)
    new_id = projectcursor.fetchone()[0]
    db_conn.commit()
    projectcursor.close()
    return new_id


def registreer_processor(identifier):
    new_id = 0
    values = (identifier, new_id)
    sql = 'CALL registreer_processor(%s, %s)'
    projectcursor = db_conn.cursor()
    projectcursor.execute(sql, values)
    new_id = projectcursor.fetchone()[0]
    db_conn.commit()
    projectcursor.close()
    return new_id


def deregistreer_processor(identifier):
    new_id = 0
    values = (identifier)
    sql = 'CALL deregistreer_processor(%s)'
    projectcursor = db_conn.cursor()
    projectcursor.execute(sql, [identifier])
    db_conn.commit()
    projectcursor.close()


def close_connection():
    if db_conn:
        db_conn.close()
