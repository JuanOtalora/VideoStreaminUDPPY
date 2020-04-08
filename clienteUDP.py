import socket
import numpy
import time
import cv2

UDP_IP = "157.253.218.204"
UDP_PORT = 5005
# SIZE = 46080
SIZE = 7680
PEDAZOS = 30

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))

s=""
finished = False

# arr = []

while not finished:

	data, addr = sock.recvfrom(SIZE)
	# print len(data)
	if data.startswith("CUADRO"):
		# print data
		pass
	elif data != "END":
		# print len(data)

		s += data

		if len(s) == (SIZE*PEDAZOS):
			print ("RECEIVED frame")

			frame = numpy.fromstring(s,dtype=numpy.uint8)
			# print (frame.shape)
			frame = frame.reshape(240,320,3)
			# arr.append(frame)
			# print "PRE W: " + str(len(frame)) + " H: " + str(len(frame[0])) 

			cv2.imshow('frame',frame)

			s=""

		if cv2.waitKey(1) & 0xFF == ord ('q'):
			break
	else:
		finished = True
		# cv2.destroyAllWindows()

# print "TRANSMITION ENDED"

# for frame in arr:
# 	cv2.imshow('frame',frame)
# 	if cv2.waitKey(1) & 0xFF == ord ('q'):
# 		break

# cv2.destroyAllWindows()

