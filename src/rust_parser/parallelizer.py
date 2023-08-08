import logging
import multiprocessing as mp
import os
import uuid
from datetime import datetime

from src.rust_parser import rustParser
from src.utils import configurator


# start_extraction starts in a new process.
# Therefore, it needs a new logging file.
def _start_parsing(nummer=0):
    process_identifier = str(uuid.uuid4())
    dt = datetime.now()
    loglevel = configurator.get_module_configurationitem(module='rust_parser', entry='loglevel')
    oude_processtap = configurator.get_module_configurationitem(module='rust_parser', entry='vorige_stap')
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log',
                                             're_processor.' + dt.strftime(
                                                 '%y%m%d-%H%M%S') + '.' + process_identifier + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=loglevel, encoding='utf-8')
    logging.info('start process ' + str(nummer) + '  with id: ' + process_identifier)
    rustParser.parse_fulltext(process_identifier)

# start_processen is the entry point for parallelizer
# it starts a configurable number of processes
def start_rust_parsing_processen():
    number_of_processes = int(configurator.get_module_configurationitem(module='rust_parser', entry='run_parallel'))
    logging.info("Number of (virtual) processors on this machine: " + str(mp.cpu_count()))
    logging.info('Starting ' + str(number_of_processes) + ' processes')
    mp.Pool()
    pool = mp.Pool(number_of_processes)
    pool.map(_start_parsing, range(number_of_processes))
    pool.close()
