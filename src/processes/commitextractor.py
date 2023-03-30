import os
from datetime import datetime
import logging
from pydriller import Repository

from src.models.models import CommitInfo, BestandsWijziging
from src.processes import hashing
from git import GitCommandError

GITHUB = 'https://github.com/'

wanted_file_types = ['.go', '.md', '.exs', '.ex', '.java', '.xml']


def extract_repository(projectname, project_id, extended=False):
    start = datetime.now()
    logging.info('start verwerking (' + str(project_id) + '):  ' + projectname + str(start))
    try:
        full_repository = Repository(GITHUB + projectname)
        for commit in full_repository.traverse_commits():
            try:
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
                        save_bestandswijziging(file, commit_info.id, extended)
                except UnicodeDecodeError as e_inner:
                    logging.exception(e_inner)
                except ValueError as e_inner:
                    logging.exception(e_inner)
                except AttributeError as e_inner:
                    logging.exception(e_inner)
            except ValueError as e_inner:
                logging.exception(e_inner)
    except GitCommandError as e_inner:
        logging.exception(e_inner)

    eind = datetime.now()
    logging.info('einde verwerking ' + projectname + str(eind))
    print(eind)
    duur = eind - start
    logging.info('verwerking ' + projectname + ' duurde ' + str(duur))
    print(duur)


def save_bestandswijziging(file, commit_id, extended=False):
    fs = file_selector(file)
    if fs[0]:
        file_changes = BestandsWijziging()
        file_changes.filename = file.filename
        file_changes.difftext = file.diff
        file_changes.idcommit = commit_id
        file_changes.locatie = file.new_path
        file_changes.extensie = fs[1]
        if extended:
            file_changes.tekstachteraf = file.content
        try:
            file_changes.save()
        except UnicodeDecodeError as e_inner:
            logging.exception(e_inner)
        except ValueError as e_inner:
            logging.exception(e_inner)


def file_selector(file):
    split_up = os.path.splitext(file.filename)
    try:
        return (file.filename == 'pom.xml' and file.new_path == '' and file.old_path == '') \
            or split_up[1] in wanted_file_types, split_up[1]
    except ValueError:
        return False
