import logging

import psycopg2

from src.utils import configurator

global db_conn


def _get_connection():
    params = configurator.get_database_configuration()
    conn = psycopg2.connect(host=params.get('host'), port=params.get('port'), user=params.get('user'),
                            password=params.get('password'), database=params.get('database'),
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


def volgend_project(processor, oude_processtap, nieuwe_processtap, connection=None):
    new_id = 0
    rowcount = 0
    projectnaam = ''

    values = (processor, oude_processtap, nieuwe_processtap, new_id, projectnaam, rowcount)
    sql = 'CALL verwerk_volgend_project(%s, %s, %s, %s, %s, %s)'
    projectcursor = db_conn.cursor() if connection is None else connection.cursor()
    projectcursor.execute(sql, values)
    resultaat = projectcursor.fetchone()
    logging.info(processor + ' heeft project opgevraagd met als resultaat: ' + str(resultaat))
    db_conn.commit() if connection is None else connection.commit()
    projectcursor.close()
    if resultaat[2] == 0 and resultaat[0] is not None and resultaat[0] > 0:
        # bug racecondition: probeer opnieuw
        return volgend_project(processor, oude_processtap, nieuwe_processtap, connection)

    return resultaat


def registreer_verwerking(projectnaam, processor, verwerking_status, projectid, connection=None):
    logging.info(processor + ' heeft project: ' + projectnaam + ' verwerkt met status: ' + verwerking_status)
    values = (projectid, verwerking_status)
    sql = 'CALL registreer_verwerking(%s, %s)'
    verwerkingcursor = db_conn.cursor() if connection is None else connection.cursor()
    verwerkingcursor.execute(sql, values)
    db_conn.commit() if connection is None else connection.commit()
    verwerkingcursor.close()


def registreer_processor(identifier, connection=None):
    new_id = 0
    values = (identifier, new_id)
    sql = 'CALL registreer_processor(%s, %s)'
    projectcursor = db_conn.cursor() if connection is None else connection.cursor()
    projectcursor.execute(sql, values)
    new_id = projectcursor.fetchone()[0]
    db_conn.commit() if connection is None else connection.commit()
    projectcursor.close()
    return new_id


def deregistreer_processor(identifier, connection=None):
    sql = 'CALL deregistreer_processor(%s)'
    projectcursor = db_conn.cursor() if connection is None else connection.cursor()
    projectcursor.execute(sql, [identifier])
    db_conn.commit() if connection is None else connection.commit()
    projectcursor.close()


def close_connection():
    if db_conn:
        db_conn.close()


def clean_testset():
    cursor = db_conn.cursor()
    sql = 'delete from test.verwerk_project;' \
          'delete from test.processor;' \
          'delete from test.bestandswijziging_zoekterm;' \
          'delete from test.bestandswijziging_info;' \
          'delete from test.bestandswijziging;' \
          'delete from test.commitinfo;' \
          'delete from test.project;' \
          'delete from test.selectie;'
    cursor.execute(sql, [])
    db_conn.commit()
    cursor.close()


def insert_3_test_projecten():
    cursor = db_conn.cursor()
    sql = "INSERT INTO selectie(selectionmoment, language, locatie) VALUES('2023-06-15', 'Java','https://onzin.com/');" \
          "INSERT INTO project(naam, idselectie, main_language)VALUES('openda-association/openda', (select max(id) from selectie), 'Java');" \
          "INSERT INTO project(naam, idselectie, main_language)VALUES('ladieda/openda', (select max(id) from selectie), 'Java');" \
          "INSERT INTO project(naam, idselectie, main_language)VALUES('quota-association/openda', (select max(id) from selectie), 'Java');"
    cursor.execute(sql, [])
    db_conn.commit()
    cursor.close()
