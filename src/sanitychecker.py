import logging

from src import hashing, db_postgresql, configurator


# check_connection checks if it is possible to connect to the database with the parameters given in the ini file.
# return true is connection is made, false otherwise.
def _check_connection() -> bool:
    return db_postgresql.check_connection()


# check_seed checks if the correct seed is being used. If another seed is used, this check has to be altered.
# return true if hashing a known string returns the expected result, false otherwise.
def _check_seed() -> bool:
    verwacht = '50fc4dda8b91cda4664edc536b472f225c7731b35f4af7a47b11d7fa2e7ec208'

    try:
        resultaat = hashing.make_hash(plaintext='test dit')
        check_result = (verwacht == resultaat)
    except Exception as e:
        logging.exception(e)
        check_result = False

    return check_result


# check_parallelization checks if the parameter for the number of processes is correctly configured.
# return true if it is a positive number 1 or bigger, false otherwise.
def _check_parallelization() -> bool:
    # check if number for parallelization is configured
    try:
        number_of_processes = configurator.get_number_of_processes()
    except Exception as e:
        logging.exception(e)
        number_of_processes = 0
    return number_of_processes > 0


# check_dependencies runs all checks, and logs their results.
# return true if all checks succeed, false otherwise.
def check_dependencies() -> bool:
    checkall = True

    # controle of database connectie werkt
    check_value = _check_connection()
    logging.info('Checking: check connection to database........[' + str(check_value) + ']')
    checkall = checkall and check_value
    # controle of seed aanwezig is
    check_value = _check_seed()
    logging.info('Checking: check seed..........................[' + str(check_value) + ']')
    checkall = checkall and check_value
    # controle of parallelization is geconfigureerd
    check_value = _check_parallelization()
    logging.info('Checking: check parallelization...............[' + str(check_value) + ']')
    checkall = checkall and check_value

    return checkall
