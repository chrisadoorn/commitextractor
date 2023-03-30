import json
import logging
import os
from datetime import datetime

from src.models.models import Selectie
from src.utils import configurator, db_postgresql

global connection


#####################################
#         define functions          #
#####################################
def read_json(jsonfile):
    if os.path.isfile(jsonfile):
        f = open(jsonfile)

        # store the deserialized JSON-encoded in the variable data
        data = json.load(f)
        f.close()
        return data
    else:
        logging.error('Het bestand ' + str(jsonfile) + ' kan niet gevonden worden')


def import_projects(jsondata, conn, selectie_id):
    logging.info('Starting import_projects for selectie: ' + str(selectie_id))
    # get data from json
    for project in jsondata['items']:
        v_name = project['name']
        v_is_fork = project['isFork']
        v_contributors = project['contributors']
        v_license = project['license']
        v_forks = project['forks']
        v_size = project['size']
        v_created_at = project['createdAt']
        v_mainlanguage = project['mainLanguage']
        v_lastcommit = project['lastCommit']
        v_no_languages = len(project['languages'])
        v_languages = project['languages']

        sql_fields = "INSERT INTO project (naam, idselectie, main_language, is_fork, license, forks," \
                     " contributors, project_size, create_date, last_commit, number_of_languages, languages"
        sql_values = ") values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        sql_return = " returning id"
        cursor = conn.cursor()
        sql = sql_fields + sql_values + sql_return
        logging.debug('sql = ' + sql)
        value_tuple = (v_name, selectie_id, v_mainlanguage, v_is_fork, v_license, v_forks, v_contributors, v_size
                       , v_created_at, v_lastcommit, v_no_languages, str(v_languages))
        cursor.execute(sql, value_tuple)
        conn.commit()
        new_id = cursor.fetchone()[0]
        logging.info('project id = ' + str(new_id))
        cursor.close()

        # insert project_verwerk
        sql_fields = "INSERT INTO verwerk_project (id, naam"
        sql_values = ") values (%s, %s) "
        cursor = conn.cursor()
        sql = sql_fields + sql_values
        logging.debug('sql = ' + sql)
        value_tuple = (new_id, v_name)
        cursor.execute(sql, value_tuple)
        conn.commit()
        cursor.close()


def import_selectioncriteria(jsondata, conn):
    logging.info('Starting import_selectioncriteria')

    v_language = None
    v_commits_min = None
    v_contributors_min = None
    v_exclude_forks = None
    v_only_forks = None
    v_has_issues = None
    v_has_pulls = None
    v_has_wiki = None
    v_has_license = None
    v_committed_min = None
    # get data from json
    for param in jsondata['parameters']:
        logging.debug('param: ' + str(param))
        match param:
            case 'commitsMin':
                v_commits_min = jsondata['parameters'][param]
            case 'contributorsMin':
                v_contributors_min = jsondata['parameters'][param]
            case 'language':
                v_language = jsondata['parameters'][param]
            case 'excludeForks':
                v_exclude_forks = jsondata['parameters'][param]
            case 'onlyForks':
                v_only_forks = jsondata['parameters'][param]
            case 'hasIssues':
                v_has_issues = jsondata['parameters'][param]
            case 'hasPulls':
                v_has_pulls = jsondata['parameters'][param]
            case 'hasWiki':
                v_has_wiki = jsondata['parameters'][param]
            case 'hasLicense':
                v_has_license = jsondata['parameters'][param]
            case 'committedMin':
                v_committed_min = jsondata['parameters'][param]

    # database part
    selectie = Selectie()
    selectie.selectionmoment = datetime.now().strftime("%Y-%m-%d")
    selectie.language = v_language
    selectie.commitsminimum = v_commits_min
    selectie.contributorsminimum = v_contributors_min
    selectie.excludeforks = v_exclude_forks
    selectie.onlyforks = v_only_forks
    selectie.hasissues = v_has_issues
    selectie.haspulls = v_has_pulls
    selectie.haswiki = v_has_wiki
    selectie.haslicense = v_has_license
    selectie.committedmin = v_committed_min

    try:
        selectie.save()
    except ValueError as e:
        logging.exception(e)
        exit(1)

    return selectie.id


def load_importfile(importfile):
    logging.info('Starting load ' + importfile)
    global connection
    connection = db_postgresql.open_connection()

    logging.info('start importing ' + importfile)
    data = read_json(importfile)
    if not data:
        logging.error('geen data gevonden')
        exit(1)

    selectie_id = import_selectioncriteria(data, connection)
    logging.debug('selectie id = ' + str(selectie_id))
    import_projects(data, connection, selectie_id)

    db_postgresql.close_connection()
    configurator.set_ghsearch_import_wanted(False)


def load():
    load_importfile(configurator.get_ghsearch_importfile())


#####################################
#         start of code             #
#####################################

def initialize():
    global filename
    # initialiseer logging
    dt = datetime.now()
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '..', '..', 'log', 'main.' + dt.strftime('%y%m%d-%H%M%S') + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')


if __name__ == '__main__':
    initialize()

    load()
