#!/usr/bin/env python3

import socketserver
from main.MainWindow import FILE_PREFIX

class SyslogUDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		print("%s:%i : " % self.server.server_address, str(data))

def setup(host='localhost', port=1024):
	print("PySysLogQt CLI Server")
	if host.startswith(FILE_PREFIX):
		filename = host[len(FILE_PREFIX):]
		with open(filename) as file:
			line = 0
			for data in file:
				line += 1
				print("%s:%i : " % (filename, line), str(data), end='')
		return
	try:
		server = socketserver.UDPServer((host, port), SyslogUDPHandler)
		print("Started SysLog Server on '%s:%i'." % (host, port))
		server.serve_forever(poll_interval=0.5)
	except PermissionError as e:
		print("You have no permission to listen on this port.\n"
			  "The ports below 1024 require root access.")
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print("Ctrl+C Pressed. Shutting down...")

if __name__ == "__main__":
	setup()
