import logging
import multiprocessing as mp
import os
import uuid
from datetime import datetime

from src.java_parsing import java_parser
from src.utils import configurator


# start_extraction starts in a new process.
# Therefore, it needs a new logging file.
def _start_diff_analysis(nummer=0):
    process_identifier = str(uuid.uuid4())
    dt = datetime.now()
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log',
                                             'processor.' + dt.strftime(
                                                 '%y%m%d-%H%M%S') + '.' + process_identifier + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    logging.info('start process ' + str(nummer) + '  with id: ' + process_identifier)
    java_parser.analyze(process_identifier)


# start_processen is the entry point for parallelizer
# it starts a configurable number of processes
def start_diff_analysis_processen():
    number_of_processes = configurator.get_number_of_processes()
    logging.info("Number of (virtual) processors on this machine: " + str(mp.cpu_count()))
    logging.info('Starting ' + str(number_of_processes) + ' processes')
    _start_diff_analysis(number_of_processes)

    # mp.Pool()
    # pool = mp.Pool(number_of_processes)
    # pool.map(_start_diff_analysis, range(number_of_processes))
    # pool.close()
