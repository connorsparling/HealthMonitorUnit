#!/usr/bin/env python3

import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with http.server.HTTPServer(("",PORT), Handler) as httpd:
	print("Listening on port", PORT)
	httpd.serve_forever()

