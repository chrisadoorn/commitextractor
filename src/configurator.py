from configparser import ConfigParser

INI_FILE = '../var/commitextractor.ini'
POSTGRESQL = 'postgresql'
PROCESS = 'process'
RUN_PARALLEL = 'run_parallel'

# get_number_of_processes returns the number of processes for which the application is configured
def get_number_of_processes():
    config = ConfigParser()
    config.read(INI_FILE)

    # get section
    if config.has_option(PROCESS, RUN_PARALLEL):
        number_of_processes = config[PROCESS][RUN_PARALLEL]
    else:
        raise Exception('Option {0} not found in the {1} file'.format(RUN_PARALLEL, INI_FILE))

    return int(number_of_processes)

# get_database_configuration returns a list of database connection parameters
def get_database_configuration():
    config = ConfigParser()
    config.read(INI_FILE)

    db = {}
    if config.has_section(POSTGRESQL):
        params = config.items(POSTGRESQL)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(POSTGRESQL, INI_FILE))

    return db
