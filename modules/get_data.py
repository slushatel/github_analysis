from modules import google_client


class GetData:
    _google_client = google_client.GoogleClient()

    # def get_example_data(self):
    #     return '{"data": 1}'.encode()

    # def get_stackoverflow_sample_repos(self):
    #     return self._google_client.get_stackoverflow_sample_repos()
    #
    # def get_github_sample_repos(self):
    #     return self._google_client.get_github_sample_repos()

    def runQuery(self, query):
        return self._google_client.runQuery(query)