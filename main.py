from src import utils, sanitychecker, db_postgresql

global logfile
global db_conn
logfile = open('log/app.log', "a")
utils.log(logfile, 'Starting application commitextractor')

try:
    # check if environment is configured properly
    sane = sanitychecker.check_dependencies(logfile)
    if not sane:
        utils.log(logfile, 'Er zijn fouten geconstateerd tijdens de initialisatie. Het programma wordt afgebroken.')
        raise Exception('Er zijn fouten geconstateerd tijdens de initialisatie. Het programma wordt afgebroken.')

    # connect to database
    db_conn = db_postgresql.get_connection()


finally:
    utils.log(logfile, 'Stopping application commitextractor')
    logfile.close()
    db_conn.close()
