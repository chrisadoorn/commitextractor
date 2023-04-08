import json
import time
from datetime import datetime, timedelta

import requests

from src.utils import configurator

GITHUB_API_ALL = 'https://api.github.com/repos/{}/commits'
GITHUB_API = 'https://api.github.com/repos/{}/commits/{}'

bearer_token = configurator.get_github_personal_access_token()

HEADERS = {"Accept": "application/vnd.github.text-match+json", "Content-Type": "text/plain;charset=UTF-8",
           "timeout": str(10), "Authorization": "Bearer {}".format(bearer_token)}

current_ratelimit_remaining = 60
reset_date_time = datetime.now() + timedelta(hours=1)


class ApiCommitRequester:

    @staticmethod
    def get_all(project):
        githubapi = GITHUB_API_ALL.format(project)
        response = requests.get(githubapi, headers=HEADERS)
        return response.json(), response.headers

    @staticmethod
    def get_specific(project, commit_sha):
        githubapi = GITHUB_API.format(project, commit_sha)
        response = requests.get(githubapi, headers=HEADERS)
        return response.json(), response.headers


class ExtractHeader:
    @staticmethod
    def get_ratelimit_remaining(headers: dict[str, str]):
        global current_ratelimit_remaining
        global reset_date_time
        current_ratelimit_remaining = int(headers.get('X-RateLimit-Remaining'))
        reset_date_time = datetime.fromtimestamp(float(headers.get('X-RateLimit-Reset')))


class ExtractContent:
    @staticmethod
    def get_content(json_: json):
        list_of_author_data = []
        error = ""
        for item in json_:
            commit_sha = item.get('sha')
            try:
                author_login = item.get('author').get('login')
                author_id = item.get('author').get('id')
            except AttributeError as e_inner:
                author_login = "not found in github"
                author_id = -1
                error = e_inner
            if (commit_sha, author_login, author_id) not in list_of_author_data:
                list_of_author_data.append((commit_sha, author_login, author_id))
        return list_of_author_data, error


class Extract:
    @staticmethod
    def get_json(project):
        result = ApiCommitRequester.get_all(project)
        ExtractHeader.get_ratelimit_remaining(result[1])
        return ExtractContent.get_content(result[0])


def get_author_data(project_name):
    print("processing: " + project_name)
    print(current_ratelimit_remaining)
    if current_ratelimit_remaining < 10:
        wait_seconds = (reset_date_time - datetime.now()).total_seconds()
        if wait_seconds > 0:
            print('Waiting for {} seconds'.format(wait_seconds))
            time.sleep(wait_seconds)
            print('Process continues')

    data = Extract.get_json(project_name)
    print(current_ratelimit_remaining)
    print(reset_date_time)
    return data


