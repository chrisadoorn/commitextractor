import logging
import os
import uuid
from datetime import datetime

from src.rust_sample_size import setSampleSize
from src.utils import db_postgresql, sanitychecker


#####################################
#         define functions          #
#####################################

def start_processing():
    try:
        # connect to database
        db_postgresql.open_connection()
        setSampleSize.performBernoulliSample()


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
        sane = sanitychecker.check_dependencies('repo_extractor')
        if not sane:
            logging.info('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')
            raise Exception('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')

        start_processing()

    finally:
        logging.info('Stopping module setSampling')


#####################################
#         start of code             #
#####################################
if __name__ == '__main__':
    # initialiseer logging
    instance_uuid = str(uuid.uuid4())
    # initialiseer logging
    dt = datetime.now()
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             '../..', 'log', 'main.setSampling.' + dt.strftime('%y%m%d-%H%M%S')
                                             + '.' + instance_uuid + '.log'))
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO, encoding='utf-8')

    logging.info('Starting module setSampling with procesid ' + instance_uuid)

    start_with_checks()
