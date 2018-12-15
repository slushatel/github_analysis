import os
import xml.etree.ElementTree
from pathlib import Path

import jsonpickle
import xmltodict

import tornado.ioloop
import tornado.web
from modules import get_data
from modules.helpers import response_value

import plotly

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
            # self.write('<p><a href="{}">{}</a>'.format(self.reverse_url("function", query["id"]), query["text"]))
        self.render("index.html", entries=all_queries)


class FunctionHandler(tornado.web.RequestHandler):
    def initialize(self, param1):
        self.param1 = param1

    def get(self, function_id):
        self.set_header('Content-Type', 'application/json')
        self.write(self.__get_data(function_id))

    def __get_query(self, query_id):
        for query in queries['queries']['query']:
            if query["id"] == query_id:
                return query["query_text"]

    def __get_data(self, query_id):
        query = self.__get_query(query_id)
        try:
            df = get_data.GetData().runQuery(query)
            # legend = 'Monthly Data'
            # labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
            # values = [10, 9, 8, 7, 6, 4, 7, 8]
            #
            # columns = df.columns.values;

            chart_json = df.to_json()
            response = response_value.ResponseValue().set_value(chart_json)
        except Exception as e:
            response = response_value.ResponseValue().set_error(response_value.ResponseError("", str(e)))

        data = jsonpickle.encode(response, unpicklable=False)
        return data


class ParametersHandler(tornado.web.RequestHandler):
    def initialize(self, param1):
        self.param1 = param1

    def get(self):
        self.set_header('Content-Type', 'application/json')
        parameters = []
        for query in queries['queries']['query']:
            query["reverse_url"] = self.reverse_url("function", query["id"])
            parameters.append({"id": query["id"], "text": query["text"], "reverse_url": query["reverse_url"]})
        self.write(jsonpickle.encode(parameters, unpicklable=False))


def get_queries_from_file():
    print("project_root: {}".format(DIR_PROJECT_ROOT))
    queries = xmltodict.parse(open(os.path.join(DIR_RESOURCES, "queries.xml")).read())
    return queries


if __name__ == "__main__":
    queries = get_queries_from_file()
    print(DIR_WEB)
    settings = {
        # "static_path": DIR_WEB,
        # "static_url_prefix": "/",
        "static_handler_args": dict(default_filename="index.html"),
    }
    app = tornado.web.Application([
        tornado.web.url(r"/function/(.*)", FunctionHandler, dict(param1='param1'), name="function"),
        tornado.web.url(r"/parameters", ParametersHandler, dict(param1='param1'), name="parameters"),
        tornado.web.url(r"/()$", tornado.web.StaticFileHandler, {'path': DIR_WEB + '\index.html'}),
        tornado.web.url(r"/(.*)", tornado.web.StaticFileHandler, {"path": DIR_WEB}),
    ], **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
