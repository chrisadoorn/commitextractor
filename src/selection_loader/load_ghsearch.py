import json
import logging
import os
from datetime import datetime

from src.models.selection_models import Selectie, Project
from src.utils import configurator


#####################################
#         define functions          #
#####################################
def __read_json(jsonfile) -> json:
    """

    :param jsonfile: relative path to jsonfile downloaded from GHSearch
    :return: The content of the file, a JSON string
    """
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),jsonfile))
    if os.path.isfile(filename):
        f = open(filename)

        # store the deserialized JSON-encoded in the variable data
        data = json.load(f)
        f.close()
        return data
    else:
        logging.error('Het bestand ' + str(jsonfile) + ' kan niet gevonden worden')
        logging.error('Het bestand ' + str(filename) + ' kan niet gevonden worden')


def import_projects(jsondata: json, selectie_id: int) -> None:
    """
    Inserts each project in the given json into the project table
    :param jsondata:
    :param selectie_id: database id for a selectie record
    """
    logging.info('Starting import_projects for selectie: ' + str(selectie_id))
    # get data from json
    for project in jsondata['items']:

        project_details = Project()
        project_details.naam = project.get('name') or None
        project_details.idselectie = selectie_id
        project_details.main_language = project.get('mainLanguage') or None
        project_details.is_fork = project.get('isFork', None)
        project_details.license = project.get('license', None) or None
        project_details.forks = project.get('forks') or None
        project_details.contributors = project.get('contributors') or None
        project_details.project_size = project.get('size') or None
        project_details.create_date = project.get('createdAt') or None
        project_details.last_commit = project.get('lastCommit') or None
        project_details.number_of_languages = len(project['languages'])
        project_details.languages = project.get('languages') or None

        try:
            project_details.save()

        except ValueError as e_outer:
            logging.exception(e_outer)


def import_selectioncriteria(jsondata: json) -> int:
    """
    inserts the used selection criteria into the selectie table.
    :param jsondata: A JSON string
    :return: id of the newly made selectie record.
    """
    logging.info('Starting import_selectioncriteria')

    selectie = Selectie()
    selectie.selectionmoment = datetime.now().strftime("%Y-%m-%d")
    selectie.language = jsondata.get('parameters').get('language') or None
    selectie.commitsminimum = jsondata.get('parameters').get('commitsMin') or None
    selectie.contributorsminimum = jsondata.get('parameters').get('contributorsMin') or None
    selectie.excludeforks = jsondata.get('parameters').get('excludeForks', None)
    selectie.onlyforks = jsondata.get('parameters').get('onlyForks', None)
    selectie.hasissues = jsondata.get('parameters').get('hasIssues', None)
    selectie.haspulls = jsondata.get('parameters').get('hasPulls', None)
    selectie.haswiki = jsondata.get('parameters').get('hasWiki', None)
    selectie.haslicense = jsondata.get('parameters').get('hasLicense', None)
    selectie.committedmin = jsondata.get('parameters').get('committedMin') or None
    selectie.locatie = 'https://github.com/'

    try:
        selectie.save()
    except ValueError as e:
        logging.exception(e)
        exit(1)

    return selectie.id


def load_importfile(importfile: str) -> None:
    """
    Process a GHSearch JSON export file indicated by a relative path
    :param importfile:
    """
    logging.info('Start importing ' + importfile)
    data = __read_json(importfile)
    if not data:
        logging.error('geen data gevonden')
        exit(1)

    selectie_id = import_selectioncriteria(data)
    logging.debug('selectie id = ' + str(selectie_id))
    import_projects(data, selectie_id)


def __load() -> None:
    load_importfile(configurator.get_module_configurationitem(module='load_ghsearch', entry='importfile'))


def __initialize() -> None:
    """
    Initialisation actions:
    -- create logging file name
    """
    # initialiseer logging
    dt = datetime.now()
    loglevel = configurator.get_module_configurationitem(module='load_ghsearch', entry='loglevel')

    log_filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..', 'log',
                                                 'load_ghsearch.' + dt.strftime('%y%m%d-%H%M%S') + '.log'))

    logging.basicConfig(filename=log_filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=loglevel, encoding='utf-8')


#####################################
#         start of code             #
#####################################

if __name__ == '__main__':
    __initialize()
    __load()
