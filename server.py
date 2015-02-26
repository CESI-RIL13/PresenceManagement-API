#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from flask import *
from config import connexion, curseur
from models import *
import jsonpickle

app = Flask(__name__)

@app.route("/")
def hello():
    # print datetime.strptime(request.headers.get('If-Modified-Since'), "%d %b %Y %H:%M:%S GMT")
    return 'Circulez il n\'y a rien à voir !'

@app.route('/users/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/users/<identifiant>', methods = ['GET', 'PUT', 'DELETE'])
def users(identifiant=None):
    if identifiant:
        user = User()
        if request.method == 'GET':
            user.id = identifiant
            user.load()
            return user.asJson()
        elif request.method == 'POST' or request.method == 'PUT':
            user.fromJson(request.data)
            user.save()
            return 'ok'
    else :
        if request.method == 'GET':
            return jsonpickle.encode(User().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)

@app.route('/presences/', methods = ['GET', 'POST'])
def presences():
    return jsonpickle.encode(Presence().search(request.args),unpicklable=False)

@app.route('/promotions/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/promotions/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def promotions(identifiant=None):
    return

@app.route('/schedulings/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def schedulings():
    return

@app.route('/rooms/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def rooms():
    return

if __name__ == "__main__":
    app.debug = True
    app.run(host = "172.20.10.2")