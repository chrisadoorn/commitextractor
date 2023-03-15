import logging
import os
from datetime import datetime

from git import GitCommandError
from pydriller import Repository
from src.experimental.models import CommitInformation, FileChanges

wanted_file_types = ['.go', '.md', '.exs', '.ex', '.java', '.xml']


def extract_repository(projectname, project_id):
    start = datetime.now()
    logging.info('start verwerking ' + projectname + str(start))
    try:
        full_repository = Repository('https://github.com/' + projectname)
        commit_teller = 0
        for commit in full_repository.traverse_commits():
            try:
                commit_teller = commit_teller + 1
                db_commit = CommitInformation()
                db_commit.remark = commit.msg
                db_commit.commit_date_time = commit.committer_date
                db_commit.email_address = commit.author.email
                db_commit.hash_value = commit.hash
                db_commit.id_project = project_id
                db_commit.username = commit.author.name
                db_commit.save()

                try:
                    for file in commit.modified_files:
                        split_up = os.path.splitext(file.filename)
                        if split_up[1] in wanted_file_types:
                            file_changes = FileChanges()
                            file_changes.filename = file.filename
                            file_changes.extension = split_up[1]
                            file_changes.id_project = project_id
                            file_changes.diff_text = file.diff
                            file_changes.text_before = file.content_before
                            file_changes.text_after = file.content
                            file_changes.id_commit = db_commit.id
                            try:
                                file_changes.save()
                            except UnicodeDecodeError as e_inner:
                                logging.exception(e_inner)
                            except ValueError as e_inner:
                                logging.exception(e_inner)
                except ValueError as e_inner:
                    logging.exception(e_inner)
            except ValueError as e_inner:
                logging.exception(e_inner)
    except GitCommandError as e_inner:
        logging.exception(e_inner)
