import logging

import psycopg2

from src import configurator

global db_conn

DATABASE_INI = '../var/commitextractor.ini'


def get_connection():
    params = configurator.get_database_configuration()
    v_host = params.get('host')
    conn = psycopg2.connect(host=params.get('host'),
                            port=params.get('port'),
                            user=params.get('user'),
                            password=params.get('password'),
                            database=params.get('database'),
                            options="-c search_path=" + params.get('schema'))
    # evalueert naar
    # conn = psycopg2.connect(host="localhost",
    #                         database="multicore",
    #                         user="appl",
    #                         password="***")
    logging.info('opened a database connection')
    return conn


def check_connection():
    # check_connection()
    # helper function for sanity check
    conn = False
    try:
        conn = get_connection()
    except Exception as e:
        logging.error('Error connecting to database')
        logging.exception(e)
    finally:
        if conn:
            conn.close()
            conn = True

    logging.info('Created connection to database')
    return conn


def open_connection():
    # open_connection()
    # create a connection and cache this connection
    global db_conn
    db_conn = get_connection()
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


def get_next_project(projectnaam, verwerking_status):
    logging.info('Project: ' + projectnaam + ' verwerkt met status: ' + verwerking_status)
    return None


def close_connection():
    if db_conn:
        db_conn.close()
