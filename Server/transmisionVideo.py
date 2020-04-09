import os
import numpy as np
import cv2
import sys
import threading
import _thread
import socket
import sqlite3
import time

SIZE = 7680
PEDAZOS = 30

class TransmisionVideo(threading.Thread):
	"""docstring for Transmision"""
	def __init__(self,videoId):
		threading.Thread.__init__(self)
		self.videoId = videoId
		
	def run(self):
		conn = sqlite3.connect('./labredes.db')

		cur = conn.cursor()
		cur.execute("SELECT * FROM Transmision t INNER JOIN Video v on t.id_video = v.id WHERE t.id_video = ?",(self.videoId,))
		# conn.commit()
		r = [dict((cur.description[i][0], value) \
				for i, value in enumerate(row)) for row in cur.fetchall()]
		conn.close()

		cap = None

		if len(r) > 0:
			print ("VIDEO RUTA: " + str(r[0]["ruta"]))
			cap = cv2.VideoCapture(r[0]["ruta"])
			# cap = cv2.VideoCapture(0)
		cuadro = 0

		while (len(r) > 0):
			# print "AUN"

			ret, frame = cap.read()

			# print "FRAME"

			for result in r:
				udp_ip = result["ip_usuario"]
				udp_port = result["puerto"]

				if frame != None:
					# print "UDP_IP: " + str(udp_ip) + " UDP_PORT: " + str(udp_port)
					print("llega aqui")
					print ("PRE W: " + str(len(frame)) + " H: " + str(len(frame[0]))) 

					# 500*300
					frame = cv2.resize(frame, (320, 240))
					# cv2.imshow('Server',frame)

					# print "POST W: " + str(len(frame)) + " H: " + str(len(frame[0])) 

					sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
					d = frame.flatten()
					s = d.tostring()
					print (len(s))

					# cv2.imshow('Server',frame)
					for i in xrange(PEDAZOS):
						time.sleep(0.01)
						# sock.sendto("CUADRO: " + str(cuadro) + " PEDAZO: " + str(i),(udp_ip, int(udp_port)))
						sock.sendto(s[i*SIZE:(i+1)*SIZE],(udp_ip, int(udp_port)))
						# print "SECTION"

					if cv2.waitKey(1) & 0xFF == ord('q'):
						conn = sqlite3.connect('./labredes.db')
						cur = conn.cursor()

						cur.execute("DELETE FROM Transmision WHERE id_video = ?",(self.videoId,))   
						conn.commit()
						conn.close()
						break
				else:
					sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
					sock.sendto("END",(udp_ip, int(udp_port)))
					sock.sendto("END",(udp_ip, int(udp_port)))
					sock.sendto("END",(udp_ip, int(udp_port)))

					conn = sqlite3.connect('./labredes.db')
					cur = conn.cursor()

					cur.execute("DELETE FROM Transmision WHERE id_video = ?",(self.videoId,))   
					conn.commit()
					conn.close()

			# time.sleep(1)
			cuadro += 1					

			conn = sqlite3.connect('./labredes.db')
			cur = conn.cursor()

			cur.execute("SELECT * FROM Transmision WHERE id_video = ?",(self.videoId,))   
			r = [dict((cur.description[i][0], value) \
				for i, value in enumerate(row)) for row in cur.fetchall()]   
			conn.close()

		if cap != None:
			cap.release()
			cv2.destroyAllWindows()

		print ("FINISHED TRANSMITING VIDEO: " + str(self.videoId))


# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005

# cap = cv2.VideoCapture(0)

# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)

#     sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#     d = frame.flatten ()
#     s = d.tostring ()
#     for i in xrange(20):

#         sock.sendto (s[i*46080:(i+1)*46080],(UDP_IP, UDP_PORT))

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()