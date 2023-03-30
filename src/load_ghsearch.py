import logging
import os
import json
from datetime import datetime

from src import db_postgresql, configurator

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

        sql_fields = "INSERT INTO project (naam, selectie_id, main_language, is_fork, license, forks," \
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
    vandaag = datetime.now()
    v_language = None
    v_commits_min = None
    v_contributors_min = None
    v_exclude_forks = None
    v_only_forks = None
    v_has_issues = None
    v_has_pulls = None
    v_has_wiki = None
    v_has_license = None
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

    # database part
    sql_select = "INSERT INTO selectie ( selectionmoment, language, commitsMinimum, contributorsMinimum," \
                 " excludeForks, onlyForks, hasIssues, hasPulls, hasWiki, hasLicense"
    sql_values = ") values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    sql_return = " returning id"
    cursor = conn.cursor()
    sql = sql_select + sql_values + sql_return
    logging.debug('sql = ' + sql)
    values_tuple = (vandaag.strftime("%Y-%m-%d"), v_language, v_commits_min, v_contributors_min, v_exclude_forks,
                    v_only_forks, v_has_issues, v_has_pulls, v_has_wiki, v_has_license)
    cursor.execute(sql, values_tuple)
    conn.commit()
    new_id = cursor.fetchone()[0]
    logging.debug('selectie id = ' + str(new_id))

    cursor.close()

    return new_id


def load():
    logging.info('Starting load')
    global connection
    connection = db_postgresql.open_connection()
    importfile = configurator.get_ghsearch_importfile()

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


#####################################
#         start of code             #
#####################################

if __name__ == '__main__':
    # initialiseer logging
    logging.basicConfig(filename='../log/load_projects.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')

    load()
