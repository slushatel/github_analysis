from http.server import BaseHTTPRequestHandler, HTTPServer
from modules import get_data

PORT_NUMBER = 8080


# This class will handle any incoming request from
# a browser
class MyHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        print('Get request received')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Send the html message
        self.wfile.write(self.get_data())
        return

    def get_data(self):
        return get_data.GetData().get_stackoverflow_sample_repos().encode()


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), MyHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
