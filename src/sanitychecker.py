from src import hashing, utils, db_postgresql


def check_connection(logfile):
    return db_postgresql.check_connection(logfile, filename='var/database.ini')


def check_seed():
    verwacht = '50fc4dda8b91cda4664edc536b472f225c7731b35f4af7a47b11d7fa2e7ec208'
    resultaat = hashing.make_hash(plaintext='test dit')
    check_result = (verwacht == resultaat)
    return check_result


def check_dependencies(logfile):
    checkall = True

    # controle of database connectie werkt

    check_value = check_connection(logfile)
    utils.log(logfile, 'Checking: check connection to database........[' + str(check_value) + ']')
    checkall = checkall and check_value
    # controle of seed aanwezig is
    check_value = check_seed()
    utils.log(logfile, 'Checking: check seed..........................[' + str(check_value) + ']')
    checkall = checkall and check_value

    return checkall
