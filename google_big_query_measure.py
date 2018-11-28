from google.cloud import bigquery

client = bigquery.Client()

job_config = bigquery.QueryJobConfig()
job_config.dry_run = True
job_config.use_query_cache = False
query_job = client.query(
    ('SELECT name, COUNT(*) as name_count '
     'FROM `bigquery-public-data.usa_names.usa_1910_2013` '
     "WHERE state = 'WA' "
     'GROUP BY name'),
    # Location must match that of the dataset(s) referenced in the query.
    location='US',
    job_config=job_config)  # API request

# A dry run query completes immediately.
assert query_job.state == 'DONE'
assert query_job.dry_run

print("This query will process {} bytes.".format(
    query_job.total_bytes_processed))
