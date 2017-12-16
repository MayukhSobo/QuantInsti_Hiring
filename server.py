from http.server import (BaseHTTPRequestHandler,
                         HTTPServer)
import os
from trading import constants


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == '/order':
            self.wfile.write(b"<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        if self.path == '/order':
            self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")


def run(port, server_class=HTTPServer, handler_class=S):
    constants.EXCHANGE_SERVER_ID = os.getpid()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=8080)