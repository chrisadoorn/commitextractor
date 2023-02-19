import logging

from src import hashing, db_postgresql, configurator


def check_connection():
    return db_postgresql.check_connection()


def check_seed():
    # check if the correct seed is being used.
    verwacht = '50fc4dda8b91cda4664edc536b472f225c7731b35f4af7a47b11d7fa2e7ec208'
    resultaat = hashing.make_hash(plaintext='test dit')
    check_result = (verwacht == resultaat)
    return check_result


def check_parallelization():
    # check if number for parallelization is configured
    number_of_processes = configurator.get_number_of_processes()
    return number_of_processes > 0


def check_dependencies():
    checkall = True

    # controle of database connectie werkt
    check_value = check_connection()
    logging.info('Checking: check connection to database........[' + str(check_value) + ']')
    checkall = checkall and check_value
    # controle of seed aanwezig is
    check_value = check_seed()
    logging.info('Checking: check seed..........................[' + str(check_value) + ']')
    checkall = checkall and check_value
    # controle of parallelization is configured
    check_value = check_parallelization()
    logging.info('Checking: check parallelization...............[' + str(check_value) + ']')
    checkall = checkall and check_value

    return checkall
