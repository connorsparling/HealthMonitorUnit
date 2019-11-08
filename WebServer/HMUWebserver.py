from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

PORT = 8080;

class HMUHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Hello from HMU Web server!')

	def do_POST(self):
		content_length = int(self.headers['Content-length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b'This is POST request. ')
		response.write(b'Receuved: ')
		response.write(body)
		self.wfile.write(response.getvalue())


with HTTPServer(("", PORT), HMUHTTPRequestHandler) as httpd:
	print("Listening on port", PORT)
	httpd.serve_forever()
