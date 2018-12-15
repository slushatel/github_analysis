from google.cloud import bigquery
import pkgutil


class GoogleClient:
    _client = bigquery.Client()

    def runQuery(self, query):
        job_config = bigquery.QueryJobConfig()
        job_config.dry_run = True
        job_config.use_query_cache = False
        query_job = self._client.query(query,
                                       # Location must match that of the dataset(s) referenced in the query.
                                       location='US', job_config=job_config)

        # A dry run query completes immediately.
        assert query_job.state == 'DONE'
        assert query_job.dry_run
        print("This query will process {} bytes.".format(query_job.total_bytes_processed))

        # run to get data
        query_job = self._client.query(query)
        results = query_job.result()  # Waits for job to complete.
        json = results.to_dataframe().to_json()
        return json
        # for row in results:
        #     print("{} : {} views".format(row.url, row.view_count))

    # def get_stackoverflow_sample_repos(self):
    #     job_config = bigquery.QueryJobConfig()
    #     job_config.dry_run = True
    #     job_config.use_query_cache = False
    #     query_job = self._client.query(("""
    #         SELECT * FROM `bigquery-public-data.github_repos.sample_repos` order by watch_count limit 10"""),
    #                                    # Location must match that of the dataset(s) referenced in the query.
    #                                    location='US',
    #                                    job_config=job_config)
    #
    #     # A dry run query completes immediately.
    #     assert query_job.state == 'DONE'
    #     assert query_job.dry_run
    #     print("This query will process {} bytes.".format(
    #         query_job.total_bytes_processed))
    #     # exit(0)
    #
    #     query_job = self._client.query("""
    #         SELECT * FROM `bigquery-public-data.github_repos.sample_repos` order by watch_count limit 10""")
    #     results = query_job.result()  # Waits for job to complete.
    #     json = results.to_dataframe().to_json()
    #     return json
    #     # for row in results:
    #     #     print("{} : {} views".format(row.url, row.view_count))
    #
    # def get_github_sample_repos(self):
    #     job_config = bigquery.QueryJobConfig()
    #     job_config.dry_run = True
    #     job_config.use_query_cache = False
    #     query_job = self._client.query(("""
    #         SELECT repo_name, COUNT(*) watch_count
    #         FROM [githubarchive:month.201605], [githubarchive:month.201604], [githubarchive:month.201603],
    #         [githubarchive:month.201602], [githubarchive:month.201601]
    #         WHERE type="WatchEvent"
    #         GROUP BY 1 HAVING watch_count >= 2 ORDER BY watch_count DESC LIMIT 400000"""),
    #                                    # Location must match that of the dataset(s) referenced in the query.
    #                                    location='US',
    #                                    job_config=job_config)
    #
    #     # A dry run query completes immediately.
    #     assert query_job.state == 'DONE'
    #     assert query_job.dry_run
    #     print("This query will process {} bytes.".format(
    #         query_job.total_bytes_processed))
    #     # exit(0)
    #
    #     query_job = self._client.query("""
    #         SELECT repo_name, COUNT(*) watch_count
    #         FROM [githubarchive:month.201605], [githubarchive:month.201604], [githubarchive:month.201603],
    #         [githubarchive:month.201602], [githubarchive:month.201601]
    #         WHERE type="WatchEvent"
    #         GROUP BY 1 HAVING watch_count >= 2 ORDER BY watch_count DESC LIMIT 400000""")
    #     results = query_job.result()  # Waits for job to complete.
    #     json = results.to_dataframe().to_json()
    #     return json
    #     # for row in results:
    #     #     print("{} : {} views".format(row.url, row.view_count))
