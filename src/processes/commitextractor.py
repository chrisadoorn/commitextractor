from datetime import datetime
import logging
from pydriller import Repository

from src.models.models import CommitInfo, BestandsWijziging
from src.processes import hashing


def extract_repository(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))

    full_repository = Repository('https://github.com/' + projectname)
    for commit in full_repository.traverse_commits():

        commit_info = CommitInfo()
        commit_info.idproject = project_id
        commit_info.commitdatumtijd = commit.committer_date
        commit_info.hashvalue = commit.hash
        commit_info.username = hashing.make_hash(commit.author.name)
        commit_info.emailaddress = hashing.make_hash(commit.author.email)
        commit_info.remark = commit.msg

        try:
            commit_info.save()
            for file in commit.modified_files:
                save_bestandswijziging(file, commit_info.id)
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


def save_bestandswijziging(file, commit_id):
    if file.filename.endswith('.java') or (
            file.filename == 'pom.xml' and file.new_path == '' and file.old_path == ''):
        # sla op in database
        file_changes = BestandsWijziging()
        file_changes.filename = file.filename
        file_changes.difftext = file.diff
        file_changes.tekstachteraf = file.content
        file_changes.idcommit = commit_id
        file_changes.locatie = file.new_path
        try:
            file_changes.save()
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)
