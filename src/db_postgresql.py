import psycopg2
from configparser import ConfigParser

from src import utils


def get_connection(filename='var/database.ini'):
    # read connection parameters
    params = config(filename=filename)
    conn = psycopg2.connect(**params)
    # evalueert naar
    # conn = psycopg2.connect(host="localhost",
    #                         database="multicore",
    #                         user="appl",
    #                         password="appl")

    return conn


def check_connection(logfile, filename):
    utils.log(logfile, 'reading database file at ' + filename)
    conn = False
    try:
        conn = get_connection(filename)
    except Exception:
        utils.log(logfile, 'Error connecting to database')
    finally:
        if conn:
            conn.close()
            conn = True
    return conn


def config(filename='../var/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    file = open(filename, 'r')

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def insert_project(connectie, values):
    sql = 'CALL test.insert_project(%s, %s, %s)'
    projectcursor = connectie.cursor()
    projectcursor.execute(sql, values)
    resultaattuple = projectcursor.fetchone()
    connectie.commit()
    projectcursor.close()
    # geef resultaat terug
    return resultaattuple[0]
