import json
import time
from datetime import datetime, timedelta

import requests
from requests.exceptions import ConnectTimeout

from src.models.models import pg_db_schema, pg_db, CommitInfo
from src.utils import configurator

GITHUB_API_ALL = 'https://api.github.com/repos/{}/commits'
GITHUB_API = 'https://api.github.com/repos/{}/commits/{}'

bearer_token = configurator.get_github_personal_access_token()

HEADERS = {"Accept": "application/vnd.github.text-match+json", "Content-Type": "text/plain;charset=UTF-8",
           "timeout": str(10), "Authorization": "Bearer {}".format(bearer_token)}

current_ratelimit_remaining = 60
reset_date_time = datetime.now() + timedelta(hours=1)
next_page = None
last_page = None


class ApiCommitRequester:

    @staticmethod
    def get_all(project):
        githubapi = GITHUB_API_ALL.format(project)
        return ApiCommitRequester.__common_part(githubapi)

    @staticmethod
    def get_specific(project, commit_sha):
        githubapi = GITHUB_API.format(project, commit_sha)
        return ApiCommitRequester.__common_part(githubapi)

    @staticmethod
    def next_page():
        if next_page is None:
            return None
        githubapi = next_page
        return ApiCommitRequester.__common_part(githubapi)

    @staticmethod
    def __common_part(githubapi):
        try:
            response = requests.get(githubapi, headers=HEADERS, timeout=(10, 20))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except ConnectTimeout:
            raise SystemExit("Timeout on " + githubapi)
        return response.json(), response.headers


class ExtractHeader:
    @staticmethod
    def get_ratelimit_remaining(headers: dict[str, str]):
        global current_ratelimit_remaining
        global reset_date_time
        global next_page
        global last_page
        current_ratelimit_remaining = int(headers.get('X-RateLimit-Remaining'))
        reset_date_time = datetime.fromtimestamp(float(headers.get('X-RateLimit-Reset')))
        link_next_page = headers.get('Link')
        next_page = None
        last_page = None
        if link_next_page is not None:
            splitted = link_next_page.split(',')
            has_next_page = splitted[0].split(';')[1].strip() == 'rel="next"'
            has_last_page = splitted[1].split(';')[1].strip() == 'rel="last"'
            if has_last_page:
                next_page = splitted[0].split(';')[0].strip()[1:-1]
            if has_next_page:
                last_page = splitted[1].split(';')[0].strip()[1:-1]


class ExtractContent:
    @staticmethod
    def get_content(json_: json, is_list=True):
        list_of_author_data = []
        error = ""
        if is_list:
            for item in json_:
                error = ExtractContent.__common_part(error, item, list_of_author_data)
        else:
            error = ExtractContent.__common_part(error, json_, list_of_author_data)
        return list_of_author_data, error

    @staticmethod
    def __common_part(error, item, list_of_author_data):
        try:
            commit_sha = item.get('sha')
            author_login = item.get('author').get('login')
            if author_login is None:
                author_login = "no author present in github"
            author_id = item.get('author').get('id')
            if author_id is None:
                author_id = -1
        except AttributeError as e_inner:
            author_login = "no author present in github"
            commit_sha = "no sha found"
            author_id = -1
            error = e_inner
        if (commit_sha, author_login, author_id) not in list_of_author_data:
            list_of_author_data.append((commit_sha, author_login, author_id))
        return error


class Extract:
    @staticmethod
    def get_json(project):
        result = ApiCommitRequester.get_all(project)
        ExtractHeader.get_ratelimit_remaining(result[1])
        return ExtractContent.get_content(result[0])

    @staticmethod
    def get_json_one_commit(project, sha):
        result = ApiCommitRequester.get_specific(project, sha)
        ExtractHeader.get_ratelimit_remaining(result[1])
        return ExtractContent.get_content(result[0], False)

    @staticmethod
    def get_json_next_page():
        result = ApiCommitRequester.next_page()
        ExtractHeader.get_ratelimit_remaining(result[1])
        return ExtractContent.get_content(result[0])


data: tuple[list[tuple[str, str, int]], str] = ([], "")


def get_author_data_one_commit(project_name, sha):
    global data
    print("processing: " + project_name + ", commit-sha:" + sha)
    if current_ratelimit_remaining < 10:
        wait_seconds = (reset_date_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            print('Waiting for {} seconds'.format(wait_seconds))
            time.sleep(wait_seconds)
            print('Process continues')

    data = Extract.get_json_one_commit(project_name, sha)
    print("Number requests remaining: " + str(current_ratelimit_remaining))
    print("processing: " + project_name + ", commit-sha:" + sha + " finished")
    return data[0][0], data[1]


def get_author_data(project_name):
    global data
    print("Number requests remaining: " + str(current_ratelimit_remaining))
    print("processing: " + project_name)
    if current_ratelimit_remaining < 10:
        wait_seconds = (reset_date_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            print('Waiting for {} seconds'.format(wait_seconds))
            time.sleep(wait_seconds)
            print('Process continues')

    data = Extract.get_json(project_name)
    __get_author_data_next_page()
    print("processing: " + project_name + " finished")
    return data


def __get_author_data_next_page():
    global data
    if next_page is None:
        return None
    print("->processing: " + str(next_page))
    if current_ratelimit_remaining < 10:
        wait_seconds = (reset_date_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            print('Waiting for {} seconds'.format(wait_seconds))
            time.sleep(wait_seconds)
            print('Process continues')

    value = Extract.get_json_next_page()
    z: list[tuple[str, str, int]] = data[0]
    z.extend(value[0])
    y = str(data[1]) + str(value[1])
    data = (z, y)
    print("->processing page finished")
    __get_author_data_next_page()
    return data


def __update_commit_info(id_project, sha, author_id, author_login):
    to_update_commit_info = CommitInfo().select().where(
        CommitInfo.idproject == id_project, CommitInfo.hashvalue == sha).get()
    to_update_commit_info.author_id = author_id
    to_update_commit_info.author_login = author_login
    to_update_commit_info.save()


def fetch_authors_per_commit(limit=5):
    schema = pg_db_schema
    cursor = pg_db.execute_sql(
        "SELECT ci.idproject, ci.emailaddress, ci.username, ci.hashvalue, pr.naam "
        "FROM " + schema + ".commitinfo AS ci " +
        "JOIN " + schema + ".project AS pr ON ci.idproject = pr.id " +
        "WHERE author_id is null limit({});".format(limit)
    )
    for (id_project, email_address_hashed, username_hashed, sha, project_name) in cursor.fetchall():
        try:
            existing_commit_info = CommitInfo().select().where(
                CommitInfo.idproject == id_project,
                CommitInfo.username == username_hashed,
                CommitInfo.emailaddress == email_address_hashed,
                CommitInfo.author_id.is_null(False)).get()
            print(
                "[update] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            __update_commit_info(id_project, sha, existing_commit_info.author_id, existing_commit_info.author_login)
        except CommitInfo.DoesNotExist:
            print("[New] " + project_name + ", un:" + username_hashed + ", ea:" + email_address_hashed)
            (commit_sha, author_login, author_id), error = get_author_data_one_commit(project_name, sha)
            __update_commit_info(id_project, sha, author_id, author_login)
