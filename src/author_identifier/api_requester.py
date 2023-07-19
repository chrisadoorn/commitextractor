import json
import logging
import time
from datetime import datetime, timedelta

import requests
from requests.exceptions import ConnectTimeout

from src.models.extracted_data_models import pg_db_schema, CommitInfo, pg_database
from src.utils import configurator

GITHUB_API = 'https://api.github.com/repos/{}/commits/{}'

bearer_token = configurator.get_github_personal_access_token()

HEADERS = {"Accept": "application/vnd.github.text-match+json", "Content-Type": "text/plain;charset=UTF-8",
           "timeout": str(10), "Authorization": "Bearer {}".format(bearer_token)}

NO_AUTHOR_FOUND_START_ID = 900000000

current_ratelimit_remaining = 60
reset_date_time = datetime.now() + timedelta(hours=1)


class ApiCommitRequester:
    @staticmethod
    def get_github_commit_info(project, commit_sha) -> (json, dict[str, str]):
        """
        Get the commit info for a commit from GitHub.
        :param project: unique name of the project
        :param commit_sha: sha of the commit
        :return: json with the commit info and the headers of the response
        """
        githubapi = GITHUB_API.format(project, commit_sha)
        try:
            response = requests.get(githubapi, headers=HEADERS, timeout=(10, 20))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.exception(err)
            return None

        except ConnectTimeout:
            logging.error("Timeout on " + githubapi)
            return None

        return response.json(), response.headers


class Extractor:
    @staticmethod
    def get_and_set_ratelimit_remaining(headers: dict[str, str]) -> None:
        """
        Get the remaining number allowed GitHub requests and the time when the limit will be reset.
        :param headers: the headers of the response
        """
        global current_ratelimit_remaining
        global reset_date_time
        current_ratelimit_remaining = int(headers.get('X-RateLimit-Remaining'))
        reset_date_time = datetime.fromtimestamp(float(headers.get('X-RateLimit-Reset')))

    @staticmethod
    def get_content(json_: json) -> tuple[tuple[str, str, int], str]:
        """
        Get the author login and the author id from the json.
        :param json_: the json with the commit info
        :return: tuple, with a tuple with the commit sha, the author login and the author id, and the error message
            When the author login or the author id is not present in the json, the value is set to 'no author present in
            GitHub' or -1.
        """
        error = ''
        try:
            commit_sha = json_.get('sha')
            author_login = json_.get('author').get('login')
            if author_login is None:
                author_login = "no author present in github"
            author_id = json_.get('author').get('id')
            if author_id is None:
                author_id = -1
        except AttributeError as e_inner:
            author_login = "no author present in github"
            commit_sha = "no sha found"
            author_id = -1
            error = e_inner
        return (commit_sha, author_login, author_id), error


def __get_json_one_commit(project, sha) -> tuple[tuple[str, str, int], str]:
    """
    Get commit info for a commit from GitHub. The commit info is returned as a json. And gets and sets the remaining
    number of allowed GitHub requests and the time when the limit will be reset.
    :param project:
    :param sha:
    :return:
    """
    result = ApiCommitRequester.get_github_commit_info(project, sha)

    Extractor.get_and_set_ratelimit_remaining(result[1])
    return Extractor.get_content(result[0])


def __get_author_data_one_commit(project_name, sha) -> tuple[tuple[str, str, int], str]:
    """
    Retrieved the author data for a commit from GitHub.
    It gets the commit info from GitHub and extracts the author login and the author id from the json.
    :param project_name: unique name of the project
    :param sha: sha of the commit
    :return: tuple, with a tuple with the commit sha, the author login and the author id, and possibly an error message.
    """
    logging.debug("processing: " + project_name + ", commit-sha:" + sha)
    global current_ratelimit_remaining
    global reset_date_time
    if current_ratelimit_remaining < 10:
        wait_seconds = (reset_date_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            logging.info("Process is waiting: " + str(current_ratelimit_remaining))
            print('Waiting for {} seconds'.format(wait_seconds))
            time.sleep(wait_seconds)
            print('Process continues')
            logging.info("Process resumes")

    data = __get_json_one_commit(project_name, sha)
    logging.debug("Number requests remaining: " + str(current_ratelimit_remaining))
    logging.debug("processing: " + project_name + ", commit-sha:" + sha + " finished")
    return data


def __update_commit_info(commit_info_id, author_id) -> None:
    """
    Update the commitInfo record.
    """
    to_update_commit_info = CommitInfo().select().where(CommitInfo.id == commit_info_id).get()
    to_update_commit_info.author_id = author_id
    to_update_commit_info.save()


def fetch_authors_by_project(projectid) -> None:
    """
    Fetch the authors for the commits in the commitInfo table.
    If the commit info is already present in the commitInfo table, it is not fetched again.
    :param projectid:
    :param limit:
    :return:
    """

    schema = pg_db_schema

    sql = """
    SELECT ci.id, ci.idproject, ci.emailaddress, ci.username, ci.hashvalue, pr.naam 
        FROM {schema}.commitinfo AS ci 
        JOIN {schema}.project AS pr ON ci.idproject = pr.id 
    WHERE ci.idproject = {projectid} AND ci.author_id is null ORDER BY ci.username, ci.emailaddress;
    """.format(schema=schema, projectid=projectid)

    cursor = pg_database.execute_sql(sql)
    counter = 1
    temp_author_id = -1
    temp_emailaddress = ""
    temp_username = ""

    for (commit_info_id, id_project, email_address_hashed, username_hashed, sha, project_name) in cursor.fetchall():
        logging.info("Processing " + str(counter))

        # Kijk of er een commitinfo bestaat binnen hetzelfde project met dezelfde username en emailaddress
        # zo ja: gebruik de author_id van die commitinfo
        # dit voorkomt onnodige requests naar github.

        if temp_emailaddress == email_address_hashed and temp_username == username_hashed and temp_author_id >= 0:
            author_id = temp_author_id
        else:
            temp_emailaddress = email_address_hashed
            temp_username = username_hashed
            existing_commit_info = CommitInfo().select().where(CommitInfo.idproject == id_project,
                                                               CommitInfo.username == username_hashed,
                                                               CommitInfo.emailaddress == email_address_hashed,
                                                               CommitInfo.author_id.is_null(False)).get_or_none()
            if existing_commit_info is not None:
                author_id = existing_commit_info.author_id
            else:
                author_id = -1

        if author_id >= 0:
            logging.info("[update] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            __update_commit_info(commit_info_id, author_id)
        else:
            logging.info("[New] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            (commit_sha, author_login, author_id), error = __get_author_data_one_commit(project_name, sha)
            if author_id < 0:
                existing_commit_info = CommitInfo().select().where(CommitInfo.emailaddress == email_address_hashed,
                                                                   CommitInfo.author_id >= NO_AUTHOR_FOUND_START_ID).get_or_none()
                if existing_commit_info is not None:
                    author_id = existing_commit_info.author_id
                else:
                    author_id = (NO_AUTHOR_FOUND_START_ID + commit_info_id)
                logging.info("No author found in GitHub, new author id created:" + str(author_id))
            __update_commit_info(commit_info_id, author_id)
        temp_author_id = author_id
        counter += 1


if __name__ == '__main__':
    fetch_authors_by_project(5)
