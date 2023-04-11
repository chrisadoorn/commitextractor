import csv
import requests
from src.models.models import GhSearchSelection

GH_SEARCH_CSV_DOWNLOAD = "https://seart-ghs.si.usi.ch/api/r/download/csv?language={}{}"

HEADERS = {"Accept": "*/*", "Content-Type": "text/plain;charset=UTF-8",
           "timeout": str(300)}


class GhSearchSampleRequester:

    @staticmethod
    def get_sample(language):
        githubapi = GH_SEARCH_CSV_DOWNLOAD.format(language, "&excludeForks=true")
        print(githubapi)
        response = requests.get(githubapi, headers=HEADERS, verify=False)
        csv_content = response.content.decode('utf-8')
        cr = csv.reader(csv_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list[1:]:
            ghs = GhSearchSelection()
            ghs_name = row[0]
            if GhSearchSelection.select(GhSearchSelection.id).where(GhSearchSelection.name == ghs_name).count() == 0:
                print(str(ghs_name) + " is not in the database")
                ghs.name = row[0]
                ghs.is_fork = row[1]
                ghs.commits = row[2]
                ghs.branches = row[3]
                ghs.default_branch = row[4]
                ghs.releases = row[5]
                ghs.contributors = row[6]
                ghs.license = row[7]
                ghs.watchers = row[8]
                ghs.stargazers = row[9]
                ghs.forks = row[10]
                ghs.size = row[11]
                ghs.created_at = row[12]
                ghs.pushed_at = row[13]
                ghs.updated_at = row[14]
                ghs.homepage = row[15]
                ghs.main_language = row[16]
                ghs.total_issues = row[17]
                ghs.open_issues = row[18]
                ghs.total_pull_requests = row[19]
                ghs.open_pull_requests = row[20]
                ghs.last_commit = row[21]
                ghs.last_commit_sha = row[22]
                ghs.has_wiki = row[23]
                ghs.is_archived = row[24]
                ghs.sub_study = language
                ghs.save()
            else:
                print(str(ghs_name) + " is already in the database")
