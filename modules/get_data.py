from modules import google_client


class GetData:
    _google_client = google_client.GoogleClient()

    def runQuery(self, query):
        return self._google_client.runQuery(query)
