from urllib.parse import urlparse, parse_qs
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi

PORT = 80
DIRECTORY = "/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        print('Received GET Request:')
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        if parsed_url.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'message': 'Hello from the web service!', 'params': query_params}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        print('Received POST Request:')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
        )
        if 'your_field_name' in form:
            field_value = form['your_field_name'].value
            print(f'Received POST data: {field_value}')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST request received successfully')

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()