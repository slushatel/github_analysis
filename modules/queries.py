# SELECT t.repo.id, t.repo.name, sum(cast (JSON_EXTRACT_SCALAR(t.payload, '$.size') as INT64)) size
#             FROM `githubarchive.day.20160501` t
#             WHERE t.type="PushEvent"
#             and JSON_EXTRACT_SCALAR(t.payload, '$.size') is not null
#             GROUP BY t.repo.id, t.repo.name
#             ORDER BY size DESC LIMIT 400000

# select
# name, sum(bytes) as bytes
# from
#
# (SELECT t.repo_name, l.*
# FROM `bigquery-public-data.github_repos.languages` t
# JOIN UNNEST(language)
# l )
# GROUP
# BY
# name
# ORDER
# BY
# bytes
# DESC
# LIMIT
# 10

# SELECT language, SUM(bytes) bytes
# FROM `ghtorrent-bq.ght.project_languages`
# GROUP BY 1
# ORDER BY 2 DESC
# LIMIT 10