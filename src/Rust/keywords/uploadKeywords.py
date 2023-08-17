import json
import logging
import os
from datetime import datetime

from src.models.selection_models import Zoekterm
from src.utils import configurator
from src.utils import db_postgresql
from src.utils.configurator import get_database_configuration

schema = get_database_configuration().get('schema')

#####################################
#         define functions          #
#####################################
def __read_json(jsonfile) -> json:
    """
    :param jsonfile: relative path to jsonfile downloaded from pgAdmin
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

def import_keywords(jsondata: json) -> None:
    """
    Inserts each keyword in the given json into the zoekterm table
    json is the result of the following query on the database dump of crates.io on 23/07/2023
        select '.rs' as extensie, d.category as term
        from public.crates a,
	         public.crates_categories b,
	         public.categories d
        where a.id = b.crate_id
          and b.category_id = d.id
          and d.id in ('275')
    :param jsondata:
    """
    logging.info('Starting import_zoekterm')
    # get data from json
    for zoekterm in jsondata:
        zoekterm_details = Zoekterm()
        zoekterm_details.extensie = zoekterm.get('extensie') or None
        #gebruik van package in broncode wordt voorafgegaan door keyword use
        zoekterm_details.zoekwoord = "use " + zoekterm.get('zoekwoord') or None
        try:
            zoekterm_details.save()
        except ValueError as e_outer:
            logging.exception(e_outer)

def delete_records() -> None:
    """
    delete all previous records from the zoekterm table & reset ID
    """
    sql = "TRUNCATE " + schema + ".zoekterm RESTART IDENTITY"
    try:
        connection = db_postgresql.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    except Exception as e:
        logging.exception(e)

    finally:
        # Close the cursor and the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_hardcoded_keywords() -> None:
    """
    Inserts each hardcoded keyword into the zoekterm table
    """
    logging.info('Starting hardcoded insert')

    zoekterm_details = Zoekterm()
    """zoekterm_details.create(extensie=".rs", zoekwoord=".await")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::thread")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::*")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::Arc")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::Barrier")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::Mutex")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::Condvar")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::Once")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::OnceLockUse")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::RwLock")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::*")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::channel")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::Sync_channel")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::Sender")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::SyncSender")
    zoekterm_details.create(extensie=".rs", zoekwoord="use std::sync::mspc::Receiver")
    """
    zoekterm_details.create(extensie=".rs", zoekwoord="thread::spawn")
    zoekterm_details.create(extensie=".rs", zoekwoord="thread::Builder::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="Arc::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="Barrier::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="Condvar::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="Mutex::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="Once::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="OnceLock::new")
    zoekterm_details.create(extensie=".rs", zoekwoord="RwLock:: new")
    zoekterm_details.create(extensie=".rs", zoekwoord="channel()")
    zoekterm_details.create(extensie=".rs", zoekwoord="channel::")
    zoekterm_details.create(extensie=".rs", zoekwoord="sync_channel(%)")
    zoekterm_details.create(extensie=".rs", zoekwoord="sync_channel::")
    zoekterm_details.create(extensie=".rs", zoekwoord=".send(%)")
    zoekterm_details.create(extensie=".rs", zoekwoord=".recv()")

def load_importfile(importfile: str) -> None:
    """
    Process a JSON export file indicated by a relative path
    :param importfile:
    """
    logging.info('Start importing ' + importfile)
    data = __read_json(importfile)
    if not data:
        logging.error('geen data gevonden')
        exit(1)
    import_keywords(data)

def __load() -> None:
    delete_records()
    insert_hardcoded_keywords()
    load_importfile(configurator.get_module_configurationitem(module='load_keywords', entry='importfile'))

def __initialize() -> None:
    """
    Initialisation actions:
    -- create logging file name
    """
    # initialiseer logging
    dt = datetime.now()
    loglevel = configurator.get_module_configurationitem(module='load_keywords', entry='loglevel')

    log_filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                 '../..', '..', 'log',
                                                 'load_keywords.' + dt.strftime('%y%m%d-%H%M%S') + '.log'))

    logging.basicConfig(filename=log_filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=loglevel, encoding='utf-8')


#####################################
#         start of code             #
#####################################

if __name__ == '__main__':
    __initialize()
    __load()
