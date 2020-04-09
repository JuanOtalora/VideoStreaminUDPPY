import os
import json
from flask import request, abort, render_template, redirect, url_for
#from flask.ext import restful
from flask_restful import Resource, Api
#from flask.ext.restful import reqparse
from flask_restful import reqparse
from Startup import app, api
from bson.objectid import ObjectId
from transmisionVideo import TransmisionVideo
from werkzeug import secure_filename
import psycopg2
#import urlparse
from urllib.parse import urlparse
import requests
import sqlite3

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

from jinja2 import Environment, PackageLoader, FileSystemLoader
env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def show_main():   

    template = env.get_template('templates/hello.html')
    return render_template(template)

@app.route('/video', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # print request.form.get('idUsuario')
        print (file)

        if file:
            print ("IF File")
            filename = secure_filename(file.filename)
            print (filename)

            conn = sqlite3.connect('./labredes.db')

            cur = conn.cursor()
            cur.execute("INSERT INTO Video values (null,?,'25565',?)",(filename,"../videos/" + str(filename)))
            conn.commit()
            conn.close()

            file.save(os.path.join("../videos", filename))
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
                 <input type=hidden value='1' name='idUsuario'>
            </form>
            '''

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
         <input type=hidden value='1' name='idUsuario'>
    </form>
    '''

class Status(Resource):
    def get(self):
        return {
            'status': 'OK'
            # 'mongo': str(mongo.db),
        }

class Login(Resource):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('user', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('direccionIP', type=str)
        
        args = parser.parse_args()

        print (args)

        user = args["user"]
        password = args["password"]
        direccionIP = args["direccionIP"]

        conn = sqlite3.connect('./labredes.db')

        cur = conn.cursor()
        cur.execute("SELECT * FROM Usuario WHERE user = ? and password = ?", (user,password))
        # conn.commit()

        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

        theId = "null"
        if (len(r) > 0):
            theId = r[0]["id"]

        conn.close()

        return {
            'usuarioiD': theId,
            'direccionServidor' : "127.0.0.1"
        }

class Videos(Resource):
    def get(self):

        conn = sqlite3.connect('./labredes.db')

        cur = conn.cursor()
        cur.execute("SELECT * FROM Video")
        # conn.commit()

        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

        conn.close()

        return {
            "videos" : r
        }

class Listas(Resource):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('idVideos', type=list)
        parser.add_argument('nombre', type=str)
        parser.add_argument('idUsuario', type=str)
        
        args = parser.parse_args()

        print (args)

        idVideos = args["idVideos"]
        nombre = args["nombre"]
        idUsuario = args["idUsuario"]

        conn = sqlite3.connect('./labredes.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO Lista values (null,?)",(nombre,))

        lastId = cur.lastrowid
        print (lastId)

        cur.execute("INSERT INTO UsuarioLista values (?,?)",(idUsuario,lastId))

        for idV in idVideos:
            cur.execute("INSERT INTO ListaVideo values (?,?)",(lastId,idV))

        conn.commit()
        conn.close()

        return {
            "idLista" : lastId
        }  

class Usuario(Resource):
    def get(self,idUsuario):     

        conn = sqlite3.connect('./labredes.db')
        cur = conn.cursor()

        cur.execute("SELECT id_lista FROM UsuarioLista WHERE id_usuario = ? ",(idUsuario,))

        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

        listas = []

        print ("ID_LISTAS: " + str(r))

        for idLis in r:
            idL = idLis["id_lista"]
            listaObj = {}
            listaObj["id"] = idL

            cur.execute("SELECT * FROM Lista WHERE id = ? ",(idL,))

            d = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

            print (d)

            listaObj["nombre"] = d[0]["nombre"]
            listaObj["videos"] = []

            cur.execute("SELECT id_video FROM ListaVideo WHERE id_lista = ? ",(idL,))

            v = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

            print (v)
            for idVid in v:
                idV = idVid["id_video"]

                cur.execute("SELECT * FROM Video WHERE id = ? ",(idV,))

                q = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]

                if (len(q) > 0):
                    listaObj["videos"].append(q[0])

            listas.append(listaObj)

        conn.close()

        return {
            "listas" : listas
        }

class ListaVideo(Resource):
    def put(self,idLista):

        parser = reqparse.RequestParser()

        parser.add_argument('idVideos', type=list)
        
        args = parser.parse_args()
        print (args)

        idVideos = args["idVideos"]

        conn = sqlite3.connect('./labredes.db')
        cur = conn.cursor()

        for idV in idVideos:
            cur.execute("INSERT INTO ListaVideo values (?,?)",(idLista,idV))

        conn.commit()
        conn.close()

        return {
            "idLista" : idLista
        }

class Transmision(Resource):
    def post(self): 

        parser = reqparse.RequestParser()

        parser.add_argument('iDvideo', type=str)
        parser.add_argument('idUsuario', type=str)
        parser.add_argument('puerto', type=str)
        parser.add_argument('ipUsuario', type=str)
        
        args = parser.parse_args()

        print (args)

        iDvideo = args["iDvideo"]
        idUsuario = args["idUsuario"]
        puerto = args["puerto"]
        ipUsuario = args["ipUsuario"]

        conn = sqlite3.connect('./labredes.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM Transmision WHERE id_video = ?",(iDvideo,))

        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]

        if len(r) == 0:
            cur.execute("INSERT INTO Transmision values (?,?,?,?)",(iDvideo,idUsuario,puerto,ipUsuario))  
            print ("STARTING Transmision THREAD FOR: " + str(iDvideo))
            transThread = TransmisionVideo(int(iDvideo))
            transThread.start()          
        else:
            cur.execute("INSERT INTO Transmision values (?,?,?,?)",(iDvideo,idUsuario,puerto,ipUsuario))

        conn.commit()
        conn.close()

        return {
            "status" : "iniciando transmision de video con id: " + str(iDvideo) + " al usuario: " + str(idUsuario) + " con puerto UDP: " + str(puerto) + " y direccion IP: " + str(ipUsuario)
        }

api.add_resource(Status, '/status')
api.add_resource(Videos, '/videos')
api.add_resource(Login, '/login')
api.add_resource(Listas, '/lista')
api.add_resource(Usuario, '/usuario/<string:idUsuario>/listas')
api.add_resource(Transmision, '/transmision')
api.add_resource(ListaVideo, '/lista/<int:idLista>')
