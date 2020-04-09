import os
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps
import psycopg2
from urllib.parse import urlparse
import sqlite3

# DATABASE_URL = os.environ.get('DATABASE_URL')
# if not DATABASE_URL:
# DATABASE_URL = "postgres://zfonvuutpuwdlp:GW5u2_uReWy3HWe-RwRXPF6uyU@ec2-54-163-238-96.compute-1.amazonaws.com:5432/dbd9s7353lvb6q"

# conn = sqlite3.connect('Comments')
# cur = conn.cursor()

# cur.execute("SELECT * FROM comment")
# print cur.fetchone()

# conn.close()
# print res

app = Flask(__name__)

# app.config['MONGO_URI'] = MONGO_URL
# mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or { "Access-Control-Allow-Origin": "*" })
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import Startup.resources