import tornado.ioloop
import tornado.web
import get_data


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="%s">get_stackoverflow_sample_repos</a>' %
                   self.reverse_url("function", "get_stackoverflow_sample_repos"))


class FunctionHandler(tornado.web.RequestHandler):
    def initialize(self, param1):
        self.param1 = param1

    def get(self, function_id):
        self.set_header('Content-Type', 'application/json')
        self.write(self.get_data(function_id))

    def get_data(self, function_id):
        return get_data.GetData().__getattribute__(function_id)().encode()


if __name__ == "__main__":
    # app = tornado.web.Application([
    #     (r"/", MainHandler),
    # ])
    app = tornado.web.Application([
        tornado.web.url(r"/", MainHandler),
        # tornado.web.url(r"/story/([0-9]+)", FunctionHandler, dict(param1='param1'), name="story")
        tornado.web.url(r"/function/(.*)", FunctionHandler, dict(param1='param1'), name="function")
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


