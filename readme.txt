#standardSQL
--SELECT id FROM [githubarchive:day.20181214] where actor.login="slushatel" LIMIT 1000
--SELECT *  FROM `githubarchive.day.20181214` where type= "PushEvent" and actor.login="slushatel"

--SELECT * FROM `bigquery-public-data.github_repos.languages` where repo_name="Talend/connectors-se" LIMIT 1000

--Select id from `ghtorrent-bq.ght_2018_04_01.users` where login = "slushatel"
--Select id, name, language,	created_at from `ghtorrent-bq.ght_2018_04_01.projects` where owner_id = 1502510
--Select * from `ghtorrent-bq.ght_2018_04_01.project_languages` where project_id in (19418155, 2502049, 18237756, 25279965, 32219745, 32221319)
Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2017_05_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10
--Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2017_09_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10
--Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2018_04_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10

--------------------------------------------------

SELECT max(created_at) as created_at FROM [ghtorrent-bq:ght.projects]
[
  {
    "created_at": "2016-09-05 11:26:26 UTC"
  }
]
ghtorrent-bq:ght.projects is too old

SELECT max(created_at) as created_at FROM `ghtorrent-bq.ght_2018_04_01.projects`
[
  {
    "created_at": "2018-03-31 23:59:57 UTC"
  }
]
ghtorrent-bq.ght_2018_04_01 - is the last seen archive


Select id from `ghtorrent-bq.ght_2018_04_01.users` where login = "slushatel"
[
  {
    "id": "1502510"
  }
]

SELECT *  FROM `githubarchive.day.20181214` where type= "PushEvent" and actor.login="slushatel"
[
  {
    "type": "PushEvent",
    "public": "true",
    "payload": "{\"push_id\":3137742421,\"size\":1,\"distinct_size\":1,\"ref\":\"refs/heads/master\",\"head\":\"b37dd1a06352863425093db672ff85f39152e860\",\"before\":\"ca45d2c56490a1040638fd3d50a4cd49e9f3e9f3\",\"commits\":[{\"sha\":\"b37dd1a06352863425093db672ff85f39152e860\",\"author\":{\"name\":\"s.bovsunovskyi\",\"email\":\"006a4502fbb2018d474727455892e6229d15199e@globallogic.com\"},\"message\":\"consider last column of data as a camera position\",\"distinct\":true,\"url\":\"https://api.github.com/repos/slushatel/hyperplane2/commits/b37dd1a06352863425093db672ff85f39152e860\"}]}",
    "repo": {
      "id": "154847832",
      "name": "slushatel/hyperplane2",
      "url": "https://api.github.com/repos/slushatel/hyperplane2"
    },
    "actor": {
      "id": "2564120",
      "login": "slushatel",
      "gravatar_id": "",
      "avatar_url": "https://avatars.githubusercontent.com/u/2564120?",
      "url": "https://api.github.com/users/slushatel"
    },
    "org": null,
    "created_at": "2018-12-14 12:22:53 UTC",
    "id": "8754635995",
    "other": "{\"actor\":{\"display_login\":\"slushatel\"}}"
  }
]


Select id, name, language,	created_at from `ghtorrent-bq.ght_2018_04_01.projects` where owner_id = 1502510
[
  {
    "id": "19418155",
    "name": "Sash-JPA-SpringMVC",
    "language": "Java",
    "created_at": "2015-04-29 08:44:46 UTC"
  },
  {
    "id": "2502049",
    "name": "shop",
    "language": "PHP",
    "created_at": "2012-10-15 13:17:08 UTC"
  },
  {
    "id": "18237756",
    "name": "chess",
    "language": "Java",
    "created_at": "2015-04-01 11:48:54 UTC"
  },
  {
    "id": "25279965",
    "name": "android2",
    "language": "Java",
    "created_at": "2015-09-03 09:33:24 UTC"
  },
  {
    "id": "32219745",
    "name": "android_front",
    "language": null,
    "created_at": "2016-02-15 15:03:27 UTC"
  },
  {
    "id": "32221319",
    "name": "front",
    "language": null,
    "created_at": "2016-02-15 15:44:40 UTC"
  }
]

Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2018_04_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10
language,bytes
c,34610097529385
javascript,9471981541204
c++,7929589338396
java,6043854438716
html,4656632868417
php,4232896826344
python,2870439330218
c#,2088821878921
css,1419142501587
jupyter notebook,1144466233176

Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2017_09_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10
language,bytes
c,33975721425721
javascript,9072103413880
c++,7608915158598
java,5758894798223
html,4352316250182
php,4086541735284
python,2666875219812
c#,1987006245173
css,1355274152340
assembly,906339435631

Select language, SUM(bytes) bytes from `ghtorrent-bq.ght_2017_05_01.project_languages` GROUP BY language ORDER BY bytes DESC LIMIT 10
language,bytes
c,33570577654611
javascript,8500325663444
c++,7193866731632
java,5343349744183
html,4052405173652
php,3918022841014
python,2403204578402
c#,1822411938644
css,1270558514510
assembly,888849026170

top languages by percent of bytes for a year grouping by month
#standardSQL
with dataset as (
SELECT concat(FORMAT_TIMESTAMP("%Y", created_at) ,".", FORMAT_TIMESTAMP("%m", created_at)) as ym, language, sum(bytes) bytes
FROM `ghtorrent-bq.ght_2018_04_01.project_languages`
where created_at between TIMESTAMP("2017-01-01") and TIMESTAMP("2018-01-01")
group by ym, language)
, sumbytes as (select ym, sum(bytes) as sb from dataset group by ym)
, percents as(select ym , language, bytes/sb*100 perc from dataset join sumbytes using (ym))

, flatperc as (select language, sum(p1) p1,sum(p2) p2,sum(p3) p3,sum(p4) p4,sum(p5) p5,sum(p6) p6
  ,sum(p7) p7,sum(p8) p8,sum(p9) p9,sum(p10) p10,sum(p11) p11,sum(p12) p12  from (
select language, perc p1, 0 p2,0 p3,0 p4,0 p5,0 p6,0 p7,0 p8,0 p9,0 p10,0 p11,0 p12 from percents where ym = "2017.01"
union all
select language, 0, perc,0,0,0,0,0,0,0,0,0,0 from percents where ym = "2017.02"
union all
select language, 0,0, perc,0,0,0,0,0,0,0,0,0 from percents where ym = "2017.03"
union all
select language, 0,0,0, perc,0,0,0,0,0,0,0,0 from percents where ym = "2017.04"
union all
select language, 0,0,0,0, perc,0,0,0,0,0,0,0 from percents where ym = "2017.05"
union all
select language, 0,0,0,0,0, perc,0,0,0,0,0,0 from percents where ym = "2017.06"
union all
select language, 0,0,0,0,0,0, perc,0,0,0,0,0 from percents where ym = "2017.07"
union all
select language, 0,0,0,0,0,0,0, perc,0,0,0,0 from percents where ym = "2017.08"
union all
select language, 0,0,0,0,0,0,0,0, perc,0,0,0 from percents where ym = "2017.09"
union all
select language, 0,0,0,0,0,0,0,0,0, perc,0,0 from percents where ym = "2017.10"
union all
select language, 0,0,0,0,0,0,0,0,0,0, perc,0 from percents where ym = "2017.11"
union all
select language, 0,0,0,0,0,0,0,0,0,0,0, perc from percents where ym = "2017.12"
) group by language)
select * from flatperc order by (p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12) desc limit 20








