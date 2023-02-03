from datetime import datetime



def log(logfile, line):
    prefix = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
    logfile.write(prefix + line + '\n')
