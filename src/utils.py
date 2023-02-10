from datetime import datetime

global logfile


def log(line):
    prefix = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
    logfile.write(prefix + line + '\n')


def log_exception(e):
    # e is type Exception
    log('##################################### START EXCEPTION #####################################')
    logfile.write(str(e))
    log('##################################### END EXCEPTION #####################################')


def open_logfile(identifier):
    global logfile
    logfile = open('../log/app.' + identifier +'.log', 'a')


def close_logfile():
    logfile.close()
