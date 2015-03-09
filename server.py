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
            if user.load() == False:
                abort(404)
            return user.asJson(),200
        elif request.method == 'PUT':
            user.fromJson(request.data)
            user.save()
            return user.asJson()
    else :
        if request.method == 'GET':
            return jsonpickle.encode(User().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)
        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            users = []
            for entity in entities:
                user = User()
                user.fromJson(entity)
                user.save()
                users.append(user.id)
            return jsonpickle.encode(users,unpicklable=False)

@app.route('/presences/', methods = ['GET', 'POST'])
def presences():
    if request.method == 'GET':
        return jsonpickle.encode(Presence().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)
    elif request.method == 'POST' or request.method == 'PUT':
        entities = jsonpickle.decode(request.data)
        print entities
        presences = []
        for entity in entities:
            presence = Presence()
            presence.fromJson(entity)
            presence.save()
            presences.append(presences.id)
        return jsonpickle.encode(presences,unpicklable=False)

@app.route('/promotions/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/promotions/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def promotions(identifiant=None):
    if identifiant:
        promotion = Promotion()
        if request.method == 'GET':
            promotion.id = identifiant
            if promotion.load() == False:
                abort(404)
            return promotion.asJson(), 200
        elif request.method == 'PUT':
            promotion.fromJson(request.data)
            promotion.save()
            return promotion.asJson()
    else:
        if request.method == 'GET':
            return jsonpickle.encode(Scheduling().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)
        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            promotions = []
            for entity in entities:
                promotion = Promotion()
                promotion.fromJson(entity)
                promotion.save()
                promotions.append(promotion.id)
            return jsonpickle.encode(promotions,unpicklable=False)

@app.route('/schedulings/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def schedulings():
    if request.method == 'GET':
        return jsonpickle.encode(Scheduling().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)
    elif request.method == 'POST' or request.method == 'PUT':
        entities = jsonpickle.decode(request.data)
        schedulings = []
        for entity in entities:
            scheduling = Scheduling()
            scheduling.fromJson(entity)
            scheduling.save()
            schedulings.append(scheduling.id)
        return jsonpickle.encode(schedulings,unpicklable=False)

@app.route('/rooms/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def rooms():
    if request.method == 'GET':
        return jsonpickle.encode(Room().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False)
    elif request.method == 'POST' or request.method == 'PUT':
        entities = jsonpickle.decode(request.data)
        rooms = []
        for entity in entities:
            room = Room()
            room.fromJson(entity)
            room.save()
            schedulings.append(rooms.id)
        return jsonpickle.encode(rooms,unpicklable=False)

if __name__ == "__main__":
    app.debug = True
    app.run(host = "10.133.129.38")

