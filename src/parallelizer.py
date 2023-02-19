import logging
import multiprocessing as mp
import uuid

from src import commitextractor, configurator


# start_extraction starts in a new process.
# Therefore, it needs a new logging file.
def start_extraction(nummer=0):
    process_identifier = str(uuid.uuid4())
    logging.basicConfig(filename='../log/process.' + process_identifier + '.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')
    logging.info('start process ' + str(nummer) + '  with id: ' + str(process_identifier))
    commitextractor.extract_repositories(process_identifier)


# start_processen is the entry point for parallelizer
# it starts a configurable number of processes
def start_processen():
    number_of_processes = configurator.get_number_of_processes()
    logging.info("Number of (virtual) processors on this machine: " + str(mp.cpu_count()))
    logging.info('Starting ' + str(number_of_processes) + ' processes')

    mp.Pool()
    pool = mp.Pool(number_of_processes)
    pool.map(start_extraction, range(number_of_processes))
    pool.close()
