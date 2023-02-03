import psycopg2
from configparser import ConfigParser
from src import utils

global db_conn

DATABASE_INI = '../var/database.ini'


def get_connection(inifile=DATABASE_INI):
    # get_connection(inifile)
    # make a connection to a database with a configuration in a given ini file

    params = config(filename=inifile)
    conn = psycopg2.connect(**params)
    # evalueert naar
    # conn = psycopg2.connect(host="localhost",
    #                         database="multicore",
    #                         user="appl",
    #                         password="***")

    return conn


def check_connection():
    # check_connection()
    # helper function for sanity check
    conn = False
    try:
        conn = get_connection()
    except:
        utils.log('Error connecting to database')
    finally:
        if conn:
            conn.close()
            conn = True
    return conn


def open_connection():
    # open_connection()
    # create a connection and cache this connection
    global db_conn
    db_conn = get_connection()


def config(filename=DATABASE_INI, section='postgresql'):
    #
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


def get_next_project(param):
    return None
