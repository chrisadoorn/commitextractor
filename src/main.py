from src import utils, sanitychecker, db_postgresql, hashing, commitextractor
import uuid

# initialiseer logging
instance_uuid = str(uuid.uuid4())
utils.open_logfile(instance_uuid)
utils.log('Starting application commitextractor with procesid ' + instance_uuid)


#####################################
#         define functions          #
#####################################

def start_processing():
    # start_processing()
    # while there projects to analyze,
    # extract data from repositories
    try:
        # connect to database
        db_postgresql.open_connection()
        # commitextractor.test_werking()
        verwerking_status = ''
        projectname = db_postgresql.get_next_project('', verwerking_status)
        # while projectname:
        projectname = 'https://github.com/apache/nifi'
        # projectname = '/git/java/nifi'

        # we gebruiken een inner try voor het verwerken van een enkel project.
        # Als dit foutgaat, dan kan dit aan het project liggen.
        # We stoppen dan met dit project, en starten een volgend project
        try:
            verwerking_status = 'mislukt'
            commitextractor.extract_repository(projectname)
            verwerking_status = 'verwerkt'
        # continue processing next project
        except Exception as e_inner:
            utils.log('Er zijn fouten geconstateerd tijdens de verwerking project. Zie details hieronder')
            utils.log_exception(e_inner)

        projectname = db_postgresql.get_next_project(projectname, verwerking_status)
    except Exception as e_outer:
        # stop processing
        utils.log('Er zijn fouten geconstateerd tijdens de initialisatie. Het programma wordt afgebroken. Zie details hieronder')
        utils.log_exception(e_outer)

    finally:
        utils.log('Cleaning up')


def start_with_checks():
    # start_with_checks()
    # check if the environment is in proper order
    # abort gracefully if it is not
    # if all is well start processing
    try:

        # cache seed value
        hashing.set_seed()
        # check if environment is configured properly
        sane = sanitychecker.check_dependencies()
        if not sane:
            utils.log('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')
            raise Exception('Er zijn fouten geconstateerd tijdens de controle. Het programma wordt afgebroken.')

        start_processing()

    finally:
        utils.log('Stopping application commitextractor')
        utils.close_logfile()


#####################################
#         start of code             #
#####################################
start_with_checks()
