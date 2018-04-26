#!/usr/bin/env python

import numpy as np
import subprocess
import signal
import socket
import sys
import time

# Socket server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 10000))
sock.listen(1)

if (len(sys.argv) < 5):
	print "\tUsage: python control_opt_flow.py <Control variable> <Setpoint> <Kp> <Ki>\n"
	sys.exit(0)

sp = float(sys.argv[2])
Kp = float(sys.argv[3])
Ki = float(sys.argv[4])
P, I = 0, 0

p = subprocess.Popen(['python', 'dense_opt_flow_%s.py' % sys.argv[1]], shell=False)

# Handle CTRL+C
def interrupt_handler(signal, frame):
	p.kill()
	sock.close()
	sys.exit(0)

def saturation(var, u):
	if var == 'camera_res' or var == 'image_res':
		if u <= 100:
			u = 100
		elif u >= 500:
			u = 500
	elif var == 'update_rate':
		if u <= 0.1:
			u = 0.1
		elif u >= 10:
			u = 10
	return u

if __name__ == "__main__":
	signal.signal(signal.SIGINT, interrupt_handler)

	with open('logfile.txt', 'w') as logfile:
		s_time = time.time()
		while True:
			connection, addr = sock.accept()
			try:
				# Wait for control request
				_ = connection.recv(16)

				# Control update
				e = sp - y
				P = Kp*e
				I += Ki*e
				u = P+I

				# Control saturation
				u = saturation(sys.argv[1], u)

				# Send control signal
				connection.sendall("%f" % u)

				# Wait for output
				y = float(connection.recv(16))

				t = time.time() - s_time
				logfile.write('%f,%f,%f\n' % (t,u,y))
				print '%f,%f,%f' % (t,u,y)
			finally:
				connection.close()

	p.kill()
	sock.close()
