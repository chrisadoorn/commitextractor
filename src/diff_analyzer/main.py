import logging
import os
import uuid
from datetime import datetime
from multiprocessing import freeze_support

from src.utils import db_postgresql, sanitychecker
from src.diff_analyzer import parallelizer


#####################################
#         define functions          #
#####################################


def start_processing():
    try:
        # connect to database
        db_postgresql.open_connection()
        parallelizer.start_diff_analysis_processen()
    except Exception as e:
        # stop processing
        logging.info(
            'Er zijn fouten geconstateerd tijdens de initialisatie. '
            'Het programma wordt afgebroken. Zie details hieronder')
        logging.info('##################################### START EXCEPTION #####################################')
        logging.error(str(e))
        logging.info('##################################### END EXCEPTION #####################################')

    finally:
        logging.info('Cleaning up')


def start_with_checks():
    # start_with_checks()
    # check if the environment is in proper order
    # abort gracefully if it is not
    # if all is well start processing
    try:

        # check if environment is configured properly
        sane = sanitychecker.check_dependencies()
        if not sane:
            logging.info('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')
            raise Exception('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')

        start_processing()

    finally:
        logging.info('Stopping application commitextractor')


#####################################
#         start of code             #
#####################################
if __name__ == '__main__':
    # initialiseer logging
    instance_uuid = str(uuid.uuid4())
    # initialiseer logging
    dt = datetime.now()
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log', 'diff_analyzer.' + dt.strftime('%y%m%d-%H%M%S') + '.' + instance_uuid + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')

    logging.info('Starting application commitextractor with procesid ' + instance_uuid)

    # freeze_support om de processen parallel te kunnen laten werken.
    freeze_support()

    start_with_checks()
