from http.server import (BaseHTTPRequestHandler,
                         HTTPServer)
import os
from trading import constants
from time import sleep
import uuid
import json
from random import randint

class S(BaseHTTPRequestHandler):
    order_status = {}
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.startswith('/order/:'):
            order_id = self.path.split(':')[-1]
            status = str.encode(str(S.order_status[order_id]))
            # We are not storing all the status of the orders
            # Comment the section below to keep track of all
            # the order status till date or store into a file
            S.order_status = {}
            self.wfile.write(status)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        if self.path == '/order':
            sleep(3)
            # Fully random unique order id
            order_id = uuid.uuid4().hex
            json_data = '{"order_id":' + f' "{order_id}"' + '}'
            # order_status = {order_id: None}
            if randint(1, 10000) % 2:
                S.order_status[order_id] = False
            else:
                S.order_status[order_id] = True
            self.wfile.write(str.encode(json.dumps(json_data)))


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