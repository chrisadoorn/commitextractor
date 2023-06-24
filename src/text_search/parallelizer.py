import logging
import multiprocessing as mp
import os
import uuid
from datetime import datetime

from src.text_search.text_searcher import search_by_project
from src.utils import configurator


# start_extraction starts in a new process.
# Therefore, it needs a new logging file.
def _start_search(nummer=0):
    process_identifier = str(uuid.uuid4())
    dt = datetime.now()
    loglevel = configurator.get_module_configurationitem(module='text_search', entry='loglevel')
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log',
                                             'ts_processor.' + dt.strftime(
                                                 '%y%m%d-%H%M%S') + '.' + process_identifier + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=loglevel, encoding='utf-8')
    logging.info('start process ' + str(nummer) + '  with id: ' + process_identifier)
    search_by_project(process_identifier)


# start_processen is the entry point for parallelizer
# it starts a configurable number of processes on windows
# it starts a configurable number of threads on linux
# the called functionality therefore gets on linux applicationcontext.
# On windows it does not.
# Therefore, the called class should be self-sufficient and create it's own logfile, database connection and so on
# peewee models have a challenge because those are loaded on the startup of the program when all imports are done.
# and the peewee model starts it's own connection when loaded.
# In Windows this is no problem, because a new process is started and the file is reloaded, and a new connection made.
# On linux however, the connection comes with the already loaded connection.
def start_text_search():
    number_of_processes = int(configurator.get_module_configurationitem(module='text_search', entry='run_parallel'))
    logging.info("Number of (virtual) processors on this machine: " + str(mp.cpu_count()))
    logging.info('Starting ' + str(number_of_processes) + ' processes')
    mp.Pool()
    pool = mp.Pool(number_of_processes)
    pool.map(_start_search, range(number_of_processes))
    pool.close()
