import numpy as np
import cv2
import sys

cap = cv2.VideoCapture('prueba2.mp4')

while(cap.isOpened()):
	ret, frame = cap.read()

	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# print sys.getsizeof(frame)
	print frame

	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print "HOLA"
cap.release()
cv2.destroyAllWindows()


# class TCP_Service(threading.Thread):
# 	"""docstring for TCP_Service"""
# 	def __init__(self):
# 		threading.Thread.__init__(self)
		
# 	def run(self):
# 		print "##################################################################"
# 		s.listen(5)
# 		while True:
# 			conn = sqlite3.connect('labredes.db')

# 			c, addr = s.accept()     
# 			print 'Got TCP connection from', addr
# 			message = c.recv(8192)

# 			print 'Message: ' + str(message)

# 			vals = message.split(",")

# 			cur = conn.cursor()
# 			cur.execute("INSERT INTO Reporte (id_cliente,id,latitud,longitud,altura,velocidad,protocolo) values (?,NULL,?,?,?,?,'TCP');", (vals[0],vals[1],vals[2],vals[3],vals[4]))
# 			conn.commit()

# 			print message

# 			c.send("-Thank you for connecting")

# 			c.close()  
# 			conn.close()