import json
import logging
import os
from datetime import datetime

from src.models.models import Selectie, Project
from src.models.process_management_models import Verwerk_Project
from src.utils import configurator


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


def import_projects(jsondata, selectie_id):
    logging.info('Starting import_projects for selectie: ' + str(selectie_id))
    # get data from json
    for project in jsondata['items']:

        project_details = Project()
        project_details.naam = project['name']
        project_details.idselectie = selectie_id
        project_details.main_language = project['mainLanguage']
        project_details.is_fork = project['isFork']
        project_details.license = project['license']
        project_details.forks = project['forks']
        project_details.contributors = project['contributors']
        project_details.project_size = project['size']
        project_details.create_date = project['createdAt']
        project_details.last_commit = project['lastCommit']
        project_details.number_of_languages = len(project['languages'])
        project_details.languages = project['languages']

        try:
            project_details.save()
            # insert project_verwerk
            verwerk_details = Verwerk_Project()
            verwerk_details.id = project_details.id
            verwerk_details.naam = project_details.naam
            try:
                # verwerk_project neemt de id over van project. peewee denkt dan standaard dat het een update is.
                # met force_insert wordt een insert afgedwongen.
                verwerk_details.save(force_insert=True)
            except ValueError as e_inner:
                logging.exception(e_inner)
        except ValueError as e_outer:
            logging.exception(e_outer)


def import_selectioncriteria(jsondata):
    logging.info('Starting import_selectioncriteria')

    selectie = Selectie()
    selectie.selectionmoment = datetime.now().strftime("%Y-%m-%d")
    selectie.language = jsondata['parameters']['language']
    selectie.commitsminimum = jsondata['parameters']['commitsMin']
    selectie.contributorsminimum = jsondata['parameters']['contributorsMin']
    selectie.excludeforks = jsondata['parameters']['excludeForks']
    selectie.onlyforks = jsondata['parameters']['onlyForks']
    selectie.hasissues = jsondata['parameters']['hasIssues']
    selectie.haspulls = jsondata['parameters']['hasPulls']
    selectie.haswiki = jsondata['parameters']['hasWiki']
    selectie.haslicense = jsondata['parameters']['hasLicense']
    selectie.committedmin = jsondata['parameters']['committedMin']

    try:
        selectie.save()
    except ValueError as e:
        logging.exception(e)
        exit(1)

    return selectie.id


def load_importfile(importfile):

    logging.info('Start importing ' + importfile)
    data = read_json(importfile)
    if not data:
        logging.error('geen data gevonden')
        exit(1)

    selectie_id = import_selectioncriteria(data)
    logging.debug('selectie id = ' + str(selectie_id))
    import_projects(data, selectie_id)

    configurator.set_ghsearch_import_wanted(False)


def load():
    load_importfile(configurator.get_ghsearch_importfile())


#####################################
#         start of code             #
#####################################

def initialize():

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
