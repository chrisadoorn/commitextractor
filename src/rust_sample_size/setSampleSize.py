#after load_ghsearch.py has run, run this code to reduce the dataset to the desired sample size

import json
import os
from configparser import ConfigParser
from src.utils import configurator
from src.utils.db_postgresql import _get_new_connection
from peewee import PostgresqlDatabase

global db_connectie
params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                           host=params.get('host'), port=params.get('port'))


CONFIDENCE = 'confidencelevelSample'
GHSEARCH = 'ghsearch'

INI_FILE = \
    os.path.realpath(os.path.join(os.path.dirname(__file__), '../..', 'var', 'commitextractor2.ini'))

#####################################
#            functions              #
#####################################

#get level of confidence from commitextractor.ini
def get_confidence():
    config = ConfigParser()
    config.read(INI_FILE)
    # get section
    if config.has_option(GHSEARCH, CONFIDENCE):
        confidence = config[GHSEARCH][CONFIDENCE]
    return confidence

#total number of projects in json
def count_json():
    if os.path.isfile(configurator.get_ghsearch_importfile()):
        f = open(configurator.get_ghsearch_importfile())
        data = json.load(f)
        totNumProjects =  len(data["items"])
    return totNumProjects

#calculate sample size via Slovin’s Formula
#This is a formula about if you know nothing about your population (f.i. normal distribution pattern)
def calcSampleSize():
    N = int(count_json())
    e = (100 - int(get_confidence()))/100
    n = N / (1 + (N * (e * e)))
    return (100 - int(n/N * 100))

#Random sample using BERNOULLI method
def performBernoulliSample():
    sql1 = "DELETE FROM test.verwerk_project WHERE id IN (SELECT id FROM test.verwerk_project TABLESAMPLE BERNOULLI  (%s))"
    db_conn = _get_new_connection()
    projectcursor = db_conn.cursor()
    projectcursor.execute(sql1, [calcSampleSize()])
    db_conn.commit()
    sql2 = "DELETE FROM test.project WHERE id NOT IN (SELECT id FROM test.verwerk_project)"
    projectcursor.execute(sql2)
    db_conn.commit()
    projectcursor.close()






