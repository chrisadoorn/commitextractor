import os
from configparser import ConfigParser

GHSEARCH = 'ghsearch'
IMPORT = 'import'
IMPORTFILE = 'importfile'
EXTENSIONS = 'language'
POSTGRESQL = 'postgresql'
PROCESS = 'process'
RUN_PARALLEL = 'run_parallel'

# INI_FILE contains the default location of the configuration
INI_FILE = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '../..', 'var', 'commitextractor.ini'))

INI_FILE2 = \
    os.path.realpath(os.path.join(os.path.dirname(__file__),
                                  '../..', 'var', 'commitextractor.ini'))

global inifile
inifile = INI_FILE

global inifile2
inifile2 = INI_FILE2

# get_number_of_processes returns the number of processes for which the application is configured
def get_number_of_processes():
    config = ConfigParser()
    config.read(inifile)

    # get section
    if config.has_option(PROCESS, RUN_PARALLEL):
        number_of_processes = config[PROCESS][RUN_PARALLEL]
    else:
        raise Exception('Option {0} not found in the {1} file'.format(RUN_PARALLEL, inifile))

    return int(number_of_processes)


# get_database_configuration returns a list of database connection parameters
def get_database_configuration():
    config = ConfigParser()
    config.read(inifile)

    db = {}
    if config.has_section(POSTGRESQL):
        params = config.items(POSTGRESQL)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(POSTGRESQL, inifile))

    return db


def get_extensions():
    config = ConfigParser()
    config.read(inifile)

    if config.has_section(EXTENSIONS):
        extensions = config.get('language', 'list_extensions').replace(' ', '').split(',')
    else:
        raise Exception('Section {0} not found in the {1} file'.format(EXTENSIONS, inifile))

    return extensions

def get_keywords():
    config = ConfigParser()
    config.read(inifile)

    if config.has_section(keywords):
        extensions = config.get('keywords', 'list_keywords').replace(' ', '').split(',')
    else:
        raise Exception('Section {0} not found in the {1} file'.format(keywords, inifile2))

    return extensions

def get_files():
    config = ConfigParser()
    config.read(inifile)

    if config.has_section(EXTENSIONS):
        extensions = config.get('language', 'list_files').replace(' ', '').split(',')
    else:
        raise Exception('Section {0} not found in the {1} file'.format(EXTENSIONS, inifile))

    return extensions


# get_ghsearch_importfile returns the file from which a list of projects can be added to be extracted.
def get_ghsearch_importfile():
    config = ConfigParser()
    config.read(inifile)

    # get section
    if config.has_option(GHSEARCH, IMPORTFILE):
        path_to_file = config[GHSEARCH][IMPORTFILE]
    else:
        raise Exception('Option {0} not found in the {1} file'.format(IMPORTFILE, inifile))

    return path_to_file


def is_ghsearch_import_wanted():
    config = ConfigParser()
    config.read(inifile)

    # get section
    if config.has_option(GHSEARCH, IMPORT):
        is_import_wanted = config[GHSEARCH][IMPORT]
    else:
        raise Exception('Option {0} not found in the {1} file'.format(IMPORTFILE, inifile))

    return bool(int(is_import_wanted))


# Zet de waarde of er een nieuwe lijst van bestanden geladen moet worden.
def set_ghsearch_import_wanted(true_or_false: bool):
    config = ConfigParser()
    config.read(inifile)
    config.set(GHSEARCH, IMPORT, str(int(true_or_false)))

    with open(inifile, 'w') as configfile:
        config.write(configfile)


# set_inifile makes the ini_file dynamic.
# this function is used for test purposes only.
def set_inifile(newfile=INI_FILE):
    global inifile
    inifile = newfile
