##### GitHub repo analyser

It uses BigQuery to analyse GitHub archived data

1. Get this repo
1. Open it in your favorite Python IDE
1. Add virtual environment or use whatever you want to [resolve dependencies](#rdep)
1. Run "start_web_server_tornado.py"
1. Run your favorite browser and go to "http://localhost:8888"
1. You should see the page with clickable links

<a name="rdep"></a>To resolve dependencies you can run:
- pip install tornado
- pip install google-cloud-bigquery``

To use Google API:
- create a project and add BigQuery API to it
- setup a service account for the project and get .json file with keys
https://cloud.google.com/video-intelligence/docs/common/auth#set_up_a_service_account
- setup locally environment variable or add it to the IDE's run config
GOOGLE_APPLICATION_CREDENTIALS=path/to/keys/file.json

