import psycopg2
from configparser import ConfigParser


def get_connection():
    # read connection parameters
    params = config()
    conn = psycopg2.connect(**params)

    # conn = psycopg2.connect(host="localhost",
    #                         database="multicore",
    #                         user="appl",
    #                         password="appl")

    return conn


def config(filename='../var/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

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
