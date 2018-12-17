import os
from pathlib import Path

import jsonpickle
import xmltodict

import tornado.ioloop
import tornado.web
from modules import get_data
from modules.helpers import response_value
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

DIR_PROJECT_ROOT = (Path(__file__).parent.parent.resolve())
DIR_RESOURCES = os.path.join(DIR_PROJECT_ROOT, "resources")
DIR_WEB = os.path.join(DIR_PROJECT_ROOT, "web")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        all_queries = []
        for query in queries['queries']['query']:
            # print(query)
            query["reverse_url"] = self.reverse_url("function", query["id"])
            all_queries.append(query)
        self.render("index.html")


class FunctionHandler(tornado.web.RequestHandler):
    def initialize(self, param1):
        self.param1 = param1

    def get(self, function_id):
        self.set_header('Content-Type', 'application/json')
        self.write(self.__get_data(function_id))

    def __get_query(self, query_id):
        for query in queries['queries']['query']:
            if query["id"] == query_id:
                return query

    def __get_data(self, query_id):
        query = self.__get_query(query_id)
        try:
            df = get_data.GetData().runQuery(query["query_text"])
            chart_json = df.to_json()
            response = response_value.ResponseValue().set_value(
                {"chart_json": chart_json, "chart_title": query["title"], "chart_datasets": query["data_sets"]})
        except Exception as e:
            response = response_value.ResponseValue().set_error(response_value.ResponseError("", str(e)))

        data = jsonpickle.encode(response, unpicklable=False)
        return data


class ParametersHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        parameters = []
        for query in queries['queries']['query']:
            query["reverse_url"] = self.reverse_url("function", query["id"])
            parameters.append({"id": query["id"], "text": query["title"], "reverse_url": query["reverse_url"]})
        self.write(jsonpickle.encode(parameters, unpicklable=False))


def format_query(query):
    if 'replacements' not in query or 'replace' not in query['replacements']:
        return
    for replace in query['replacements']['replace']:
        replace_anchor = replace["replace_anchor"]
        replace_base = replace["replace_base"]
        replace_format = replace["replace_format"]
        new_value = ""

        if replace_base == "CURRENT_DATE":
            base_date = datetime.now()
            replace_relative = json.loads(replace["replace_date_relative"])
            new_value = base_date + relativedelta(**replace_relative)
        new_value = new_value.strftime(replace_format)
        query["query_text"] = query["query_text"].replace(replace_anchor, new_value)
        print(query["query_text"])


def get_queries_from_file():
    print("project_root: {}".format(DIR_PROJECT_ROOT))
    queries = xmltodict.parse(open(os.path.join(DIR_RESOURCES, "queries.xml")).read(), force_list={'replace'})
    for query in queries['queries']['query']:
        format_query(query)
    return queries


if __name__ == "__main__":
    queries = get_queries_from_file()
    print(DIR_WEB)
    app = tornado.web.Application([
        tornado.web.url(r"/function/(.*)", FunctionHandler, dict(param1='param1'), name="function"),
        tornado.web.url(r"/parameters", ParametersHandler),
        tornado.web.url(r"/(.*)", tornado.web.StaticFileHandler, {"path": DIR_WEB, "default_filename": "index.html"}),
        # tornado.web.url(r"/()$", tornado.web.StaticFileHandler, {'path': DIR_WEB + '\index.html'}),
        # tornado.web.url(r"/(.*)", tornado.web.StaticFileHandler, {"path": DIR_WEB}),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
