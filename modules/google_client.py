from google.cloud import bigquery


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
        df = results.to_dataframe()
        json = df.to_json()
        return df
        # for row in results:
        #     print("{} : {} views".format(row.url, row.view_count))
