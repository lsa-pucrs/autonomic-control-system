#!/usr/bin/env python

import cv2
import numpy as np
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import psutil
import socket
import time

# Setup camera resolution and framerate
resolution, fps = (640, 480), 30
camera = PiCamera()
camera.resolution = resolution
camera.framerate = fps
rawCapture = PiRGBArray(camera)

# Allow time for camera to warm up
time.sleep(0.1)

# Instantiate this process
proc = psutil.Process(os.getpid())

# Request control update through TCP socket (send with response)
def request_control(data, addr=('localhost', 10000)):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(addr)
	try:
		sock.sendall(data)
		resp = sock.recv(16)
	finally:
		sock.close()
	return resp

# Simply send data through TCP socket (without response)
def send_data(data, addr):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(addr)
	try:
		sock.sendall(data)
	finally:
		sock.close()

if __name__ == "__main__":
	u = 10
	y = 0

	while True:
		# Request control update (send random data to control module to request update)
		u = float(request_control('A'))
		
		# Actuate
		time.sleep(float(1/u))

		# Dynamic system
		# Get first frame
		rawCapture.truncate(0)	# Clear capture object buffer
		camera.capture(rawCapture, format='bgr')
		frame1 = rawCapture.array
		# Convert to grayscale
		prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
		
		# Get second frame
		rawCapture.truncate(0)	# Clear capture object buffer
		camera.capture(rawCapture, format='bgr')
		frame2 = rawCapture.array
		# Convert to grayscale
		nxt = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
		
		# Dense optical flow
		flow = cv2.calcOpticalFlowFarneback(prvs, nxt, 0.5, 3, 15, 3, 5, 1.2, 0)
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
		# Convert to HSV
		hsv = np.zeros_like(frame1)
		hsv[...,0] = ang*180/np.pi/2
		hsv[...,1] = 255
		hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
		bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

		# Send CPU load of this process
		send_data(proc.cpu_percent(interval=None))
