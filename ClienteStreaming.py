from tkinter import *
import requests
import cv2
import socket
import json
import numpy
import time
import threading
import _thread


class UDP_client(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		SIZE = 7680
		PEDAZOS = 30

		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.bind ((ip, UDP_PORT))

		s=""
		finished = False

		print ('voy a entrar al while de la transmision')

		cv2.startWindowThread()
		cv2.namedWindow("frame")

		while not finished:

		    data, addr = sock.recvfrom(SIZE)
		    # print len(data)

		    if data != "END":
		        s += data

		        if len(s) == (SIZE*PEDAZOS):
		            # print "RECEIVED frame"

		            frame = numpy.fromstring(s,dtype=numpy.uint8)
		            # print (frame.shape)
		            frame = frame.reshape(240,320,3)
		            # print "PRE W: " + str(len(frame)) + " H: " + str(len(frame[0]))

		            
		            cv2.imshow('frame',frame)

		            s=""

		        if cv2.waitKey(1) & 0xFF == ord ('q'):
		            break
		    else:
		        finished = True
		        print (' se acabo la transmision')
		        cv2.destroyAllWindows()

def iniciarTransmision() :
	
	SIZE = 7680
	PEDAZOS = 30

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind ((ip, UDP_PORT))

	s=""
	finished = False

	print ('voy a entrar al while de la transmision')
	cv2.startWindowThread()
	cv2.namedWindow("frame")

	while not finished:

	    data, addr = sock.recvfrom(SIZE)
	    # print len(data)

	    if data != "END":
	        s += data

	        if len(s) == (SIZE*PEDAZOS):
	            # print "RECEIVED frame"

	            frame = numpy.fromstring(s,dtype=numpy.uint8)
	            # print (frame.shape)
	            frame = frame.reshape(240,320,3)
	            # print "PRE W: " + str(len(frame)) + " H: " + str(len(frame[0]))

	            cv2.imshow('frame',frame)

	            s=""

	        if cv2.waitKey(1) & 0xFF == ord ('q'):
	            break
	    else:
	        finished = True
	        print (' se acabo la transmision')
	        cv2.destroyAllWindows()

def seleccionarVideo() :
	print ('Seleccionar video')
	global selected

	selected =  videos[int(select4.curselection()[0])]['id']

def verVideoTodos() :
	print ('Ver video todos')
	#global UDP_PORT

	#thread.start_new_thread(iniciarTransmision, ())
	
	

	
	#UDP_PORT = int(videos[int(select1.curselection()[0])]['puerto'])
	idVid = videos[int(select1.curselection()[0])]['id']

	js = {'iDvideo':idVid,'idUsuario':int(idUsuario),'puerto':UDP_PORT,'ipUsuario':ip}
	headers = {'content-type': 'application/json'}
	print ('http://'+UDP_IP+':5000/transmision')
	r = requests.post(version+UDP_IP+':5000/transmision', data=json.dumps(js), headers=headers, verify=False)
	print (r.text)

	#thr = UDP_client()
	#thr.start()
	#print 'ya se creo el thread'
	iniciarTransmision()


def verVideoLista() :
	print ('ver video Lista')

	#UDP_PORT = int(videos[int(select1.curselection()[0])]['puerto'])
	idVid = vidLista[int(select3.curselection()[0])]['id']

	js = {'iDvideo':idVid,'idUsuario':int(idUsuario),'puerto':UDP_PORT,'ipUsuario':ip}
	headers = {'content-type': 'application/json'}
	print ('http://'+UDP_IP+':5000/transmision')
	r = requests.post(version+UDP_IP+':5000/transmision', data=json.dumps(js), headers=headers, verify=False)
	print (r.text)
	iniciarTransmision()


def mostrarVideosLista() :
	print ('mostrar videos lista')
	global vidLista


	vidLista =  listas[int(select2.curselection()[0])]['videos']

	for x in range(0,len(vidLista)):
		select3.insert(0,vidLista[x]['nombre'])	

def agregarVideo() :
	print ('agregar video')

	idLista = listas[int(select5.curselection()[0])]['id']

	sele = [selected]

	js = {'idVideos':sele}
	headers = {'content-type': 'application/json'}
	r = requests.put(version+UDP_IP+':5000/lista/'+str(idLista), data=json.dumps(js), headers=headers, verify=False)
	#resp = r.json
	print (r.text)
	updateUI()

def agregarLista() :
	print ('agregar lista')
	js = {'nombre':nuevaLista.get(),'idVideos':[],'idUsuario':idUsuario}
	headers = {'content-type': 'application/json'}
	r = requests.post(version+UDP_IP+':5000/lista', data=json.dumps(js), headers=headers, verify=False)
	#resp = r.json
	print (r.text)
	updateUI()

def subirVideo() :
	print ('Subir video')
	url = version+UDP_IP+':5000/video'
	nue = nuevoVid.get()
	files = {'file': open(nue, 'rb')}
	r = requests.post(url, files=files, verify=False)
	#resp = json.loads(r.text)
	print (r.text)
	updateUI()

def pedirVideos() :
	global videos

	r = requests.get(version+UDP_IP+':5000/videos', verify=False)
	videos = json.loads(r.text)['videos']
	print (r.text)

def darListas() :
	global listas

	r = requests.get(version+UDP_IP+':5000/usuario/'+idUsuario+'/listas', verify=False)
	listas = json.loads(r.text)['listas']
	print (r.text)
	

def updateUI() :
	global select1,select2,select3,select4,select5, nuevaLista, nuevoVid ,UDP_PORT

	pedirVideos()
	darListas()


	clearFrame(frame1)
	clearFrame(frame2)
	clearFrame(frame3)
	clearFrame(frame4)
	clearFrame(frame5)
	clearFrame(frame6)
	clearFrame(frame7)
	clearFrame(frame8)
	clearFrame(frame9)
	clearFrame(frame10)
	clearFrame(frame11)

	Label(frame1, text="Ver todos los videos").grid(row=0, column=0, sticky=W)

	scroll1 = Scrollbar(frame2, orient=VERTICAL)
	select1 = Listbox(frame2, yscrollcommand=scroll1.set, height=6)
	scroll1.config (command=select1.yview)
	scroll1.pack(side=LEFT, fill=Y)
	select1.pack(side=LEFT,  fill=BOTH, expand=1)

	for x in range(0,len(videos)):
		select1.insert(x,videos[x]['nombre'])
    

	b1 = Button(frame2,text="Ver",command=verVideoTodos)
	b1.pack(side=LEFT)

	Label(frame3, text="Ver videos por lista").grid(row=0, column=0, sticky=W)

	scroll2 = Scrollbar(frame4, orient=VERTICAL)
	select2 = Listbox(frame4, yscrollcommand=scroll2.set, height=6)
	scroll2.config (command=select2.yview)
	select2.pack(side=LEFT,  fill=BOTH, expand=1)
	scroll2.pack(side=LEFT, fill=Y)

	for x in range(0,len(listas)):
		select2.insert(x,listas[x]['nombre'])

	scroll3 = Scrollbar(frame4, orient=VERTICAL)
	select3 = Listbox(frame4, yscrollcommand=scroll3.set, height=6)
	scroll3.config (command=select3.yview)
	select3.pack(side=LEFT,  fill=BOTH, expand=1)
	scroll3.pack(side=LEFT, fill=Y)

	b2 = Button(frame4,text="Mostrar",command=mostrarVideosLista)
	b2.pack(side=LEFT)
	b3 = Button(frame4,text="Ver",command=verVideoLista)
	b3.pack(side=LEFT)

	Label(frame5, text="Agregar videos a lista").grid(row=0, column=0, sticky=W)

	scroll4 = Scrollbar(frame6, orient=VERTICAL)
	select4 = Listbox(frame6, yscrollcommand=scroll4.set, height=6)
	scroll4.config (command=select4.yview)
	select4.pack(side=LEFT,  fill=BOTH, expand=1)
	scroll4.pack(side=LEFT, fill=Y)

	for x in range(0,len(videos)):
		select4.insert(x,videos[x]['nombre'])

	scroll5 = Scrollbar(frame6, orient=VERTICAL)
	select5 = Listbox(frame6, yscrollcommand=scroll5.set, height=6)
	scroll5.config (command=select5.yview)
	select5.pack(side=LEFT,  fill=BOTH, expand=1)
	scroll5.pack(side=LEFT, fill=Y)

	for x in range(0,len(listas)):
		select5.insert(x,listas[x]['nombre'])

	b90 = Button(frame6,text="Seleccionar",command=seleccionarVideo)
	b90.pack(side=LEFT)

	b4 = Button(frame6,text="Agregar",command=agregarVideo)
	b4.pack(side=LEFT)

	Label(frame7, text="Agregar lista").grid(row=0, column=0, sticky=W)

	nuevaLista = StringVar()
	name = Entry(frame8, textvariable=nuevaLista)
	name.pack(side=LEFT)

	b5 = Button(frame8,text="Agregar",command=agregarLista)
	b5.pack(side=RIGHT)

	Label(frame9, text="Subir video").grid(row=0, column=0, sticky=W)

	nuevoVid = StringVar()
	textNuevoVideo = Entry(frame10, textvariable=nuevoVid)
	textNuevoVideo.pack(side=LEFT)

	b6 = Button(frame10,text="Subir",command=subirVideo)
	b6.pack(side=RIGHT)

	b7 = Button(frame11,text="Salir",command=salir)
	b7.pack(side=RIGHT)


def clearFrame(fr) :
	for widget in fr.winfo_children():
		widget.destroy()

def salir() :
	raise SystemExit		

def login() :

	global idUsuario
    #phonelist.append ([nameVar.get(), phoneVar.get()])
    #setSelect ()
	js = {'user':nameVar.get(),'password':phoneVar.get(),'direccionIP':ip}
	headers = {'content-type': 'application/json'}
    #r = requests.get('https://github.com/timeline.json')
	r = requests.post(version+UDP_IP+':5000/login', data=json.dumps(js), headers=headers, verify=False)
	resp = json.loads(r.text)
	print (r.text)
    #ipServidor = resp['direccionServidor']
	idUsuario = str(resp['usuarioiD'])
	updateUI()

def makeWindow () :
    global nameVar, phoneVar,  ip , ipServidor , frame1 , frame2, frame3, version 
    global frame4, frame5,frame6,frame7,frame8,frame9,frame10, frame11,UDP_IP, UDP_PORT


    ip = '157.253.221.174'
    UDP_IP = "157.253.221.174"
    UDP_PORT = 5005
    win = Tk()
    version = 'http://'


    frame1 = Frame(win)
    frame1.pack()

    Label(frame1, text="Usuario").grid(row=0, column=0, sticky=W)
    nameVar = StringVar()
    name = Entry(frame1, textvariable=nameVar)
    name.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Clave").grid(row=1, column=0, sticky=W)
    phoneVar= StringVar()
    phone= Entry(frame1, textvariable=phoneVar)
    phone.grid(row=1, column=1, sticky=W)

    frame2 = Frame(win)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2,text=" Login  ",command=login)
    b1.pack(side=LEFT)
    

    frame3 = Frame(win)       
    frame3.pack()
    frame4 = Frame(win)       
    frame4.pack()
    frame5 = Frame(win)       
    frame5.pack()
    frame6 = Frame(win)       
    frame6.pack()
    frame7 = Frame(win)       
    frame7.pack()
    frame8 = Frame(win)       
    frame8.pack()
    frame9 = Frame(win)       
    frame9.pack()
    frame10 = Frame(win)       
    frame10.pack()
    frame11 = Frame(win)       
    frame11.pack()

    win.minsize(width=666, height=666)


    return win


win = makeWindow()

win.mainloop()

