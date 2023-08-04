#after load_ghsearch.py has run, run this code to reduce the dataset to the desired sample size

import json
import os
from configparser import ConfigParser
from src.utils import configurator
from src.utils.db_postgresql import _get_new_connection
from peewee import PostgresqlDatabase

global db_connectie, sample

params = configurator.get_database_configuration()
pg_db = PostgresqlDatabase(database=params.get('database'), user=params.get('user'), password=params.get('password'),
                           host=params.get('host'), port=params.get('port'))


SAMPLELEVEL = 'sampleLevel'
"""if samplelevel f.i. 90 then we keep 10% of the originals"""
GHSEARCH = 'load_ghsearch'

INI_FILE = \
    os.path.realpath(os.path.join(os.path.dirname(__file__), '../..', 'var', 'commitextractor.ini'))

#####################################
#            functions              #
#####################################

#get level of sample from commitextractor.ini
def get_sample():
    config = ConfigParser()
    config.read(INI_FILE)
    # get section
    sample = None
    if config.has_option(GHSEARCH, SAMPLELEVEL):
        sample = config[GHSEARCH][SAMPLELEVEL]
    return sample

#Random sample using BERNOULLI method
def performBernoulliSample():
    sql1 = "DELETE FROM test.verwerk_project WHERE id IN (SELECT id FROM test.verwerk_project TABLESAMPLE BERNOULLI  (%s))"
    db_conn = _get_new_connection()
    projectcursor = db_conn.cursor()
    print(get_sample())
    projectcursor.execute(sql1, [get_sample()])
    db_conn.commit()
    sql2 = "DELETE FROM test.project WHERE id NOT IN (SELECT id FROM test.verwerk_project)"
    projectcursor.execute(sql2)
    db_conn.commit()
    projectcursor.close()

if __name__ == '__main__':
    get_sample()




