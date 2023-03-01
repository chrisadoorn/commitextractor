from src import parallelizer, configurator

if __name__ == '__main__':
    configurator.inifile = '../../var/commitextractor.ini'
    parallelizer.start_processen()
