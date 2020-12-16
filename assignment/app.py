# -*- coding: utf8 -*-
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json

from assignment.transform import transform

PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data_in = json.loads(self.rfile.read(length))
        data_out = json.dumps(transform(data_in)).encode('utf8')
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data_out)))
        self.end_headers()
        self.wfile.write(data_out)


def run(server_class=ThreadingHTTPServer, handler_class=Handler):
    server_class(('', PORT), handler_class).serve_forever()


if __name__ == '__main__':
    run()
