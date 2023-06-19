import json

import requests

from src.selection_loader.load_ghsearch import import_selectioncriteria, import_projects

GH_SEARCH_CSV_DOWNLOAD = "https://seart-ghs.si.usi.ch/api/r/download/json?nameEquals=false{}{}{}{}"

HEADERS = {"Accept": "*/*", "Content-Type": "text/plain;charset=UTF-8", "timeout": str(300)}


class GhSearchSampleRequester:
    """
    This class is used to request a sample from the GHSearch API.
    It downloads the sample and saves it in the database using import_projects.
    """

    @staticmethod
    def get_sample(language, t: tuple[bool, int, int]):
        gh_search_api = GH_SEARCH_CSV_DOWNLOAD.format("&language=" + language,
                                                      "&excludeForks=" + ("true" if t[0] else "false"),
                                                      "&commitsMin=" + str(t[1]),
                                                      "&contributorsMin=" + str(t[2]))

        print(gh_search_api)
        response = requests.get(gh_search_api, headers=HEADERS, verify=False)
        content = response.content.decode('latin-1')
        data = json.loads(content)
        sel_id = import_selectioncriteria(data)
        import_projects(data, sel_id)


if __name__ == '__main__':
    print("GhSearchSampleRequester gestart.")
    g = GhSearchSampleRequester()
    g.get_sample("Elixir", (True, 10, 2))
    print("GhSearchSampleRequester klaar.")