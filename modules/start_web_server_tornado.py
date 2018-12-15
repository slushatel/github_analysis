import os
import xml.etree.ElementTree
from pathlib import Path

import jsonpickle
import xmltodict

import tornado.ioloop
import tornado.web
from modules import get_data
from modules.helpers import response_value


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        for query in queries['queries']['query']:
            print(query)
            self.write('<p><a href="{}">{}</a>'.format(self.reverse_url("function", query["id"]), query["text"]))


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
            query_result = get_data.GetData().runQuery(query)
            response = response_value.ResponseValue().set_value(query_result)
        except Exception as e:
            response = response_value.ResponseValue().set_error(response_value.ResponseError("", str(e)))

        data = jsonpickle.encode(response, unpicklable=False)
        return data


def get_queries_from_file():
    DIR_PROJECT_ROOT = (Path(__file__).parent.parent.resolve())
    print("project_root: {}".format(DIR_PROJECT_ROOT))
    DIR_RESOURCES = os.path.join(DIR_PROJECT_ROOT, "resources")
    queries = xmltodict.parse(open(os.path.join(DIR_RESOURCES, "queries.xml")).read())
    return queries


if __name__ == "__main__":
    queries = get_queries_from_file()

    app = tornado.web.Application([
        tornado.web.url(r"/", MainHandler),
        tornado.web.url(r"/function/(.*)", FunctionHandler, dict(param1='param1'), name="function")
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
