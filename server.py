#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from flask import *
from config import connexion, curseur
from models import *
import jsonpickle
import ConfigParser

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.before_request
def detect_user_login():

    if request.endpoint == 'static':
        return

    if not 'user_id' in session and request.endpoint != 'login':
        return redirect(url_for('login'))

    if 'user_id' in session and request.endpoint == 'login':
        return redirect(url_for('hello'))

@app.route("/")
def hello():
    # print datetime.strptime(request.headers.get('If-Modified-Since'), "%d %b %Y %H:%M:%S GMT")

    user = User()
    user.id = session['user_id']
    user.load()

    return 'Hello %s' % user.fullname

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.headers['Accept'].split(',')[0] == 'text/html':

        if request.method == 'GET':
            return render_template('index.html')

        if request.method == 'POST':
            user = User()
            if user.login(request.form['mail'],request.form['password']):
                session['user_id'] = user.id
                return redirect(url_for('presences'))
            else:
                return "Invalid password",401

    else:
        return 'logue toi !',401

@app.route('/users/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/users/<identifiant>', methods = ['GET', 'PUT', 'DELETE'])
def users(identifiant=None):
    if identifiant:

        user = User()

        if request.method == 'GET':
            user.id = identifiant

            try:
                user.load()

            except Error, e:
                return e.value, e.code
            else:
                if request.headers['Accept'].split(',')[0] == 'text/html':
                    if user.role == 'stagiaire' or user.role == 'intervenant':
                        return render_template('participant.html', user = user)
                    else:
                        return render_template('utilisateur.html', user = user)
                else:
                    return user.asJson(),200

        elif request.method == 'PUT':
            user.fromJson(request.data)
            try :
                user.save()

            except Error, e:
                return e.value,e.code
            else:
                return user.asJson(),201
    else :

        if request.method == 'GET':
            if request.headers['Accept'].split(',')[0] == 'text/html':
                users = User().search(request.args,request.headers.get('If-Modified-Since'))

                return render_template('utilisateurs.html', users = users)
            else:
                try:
                    return jsonpickle.encode(User().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
                except Error, e:
                    return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            users = []
            for entity in entities:
                user = User()
                user.fromJson(entity)
                try:
                    user.save()
                except Error, e:
                    return e.value,e.code

                users.append(user.id)
            return jsonpickle.encode(users,unpicklable=False),201

@app.route('/presences/', methods = ['GET', 'POST'])
def presences():
    if request.method == 'GET':
        if request.headers['Accept'].split(',')[0] == 'text/html':
            presences = []
            promotions = []

            try:
                promotions = Promotion().search()
                presences = Presence().search(request.args)
                return render_template('presences.html', presences = presences, promotions = promotions)
            except Error, e:
                print e
                presences = False
            finally:
                return render_template('presences.html', presences = presences, promotions = promotions)

        else:
            try:
                return jsonpickle.encode(Presence().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
            except Error, e:
                return e.value,e.code

    elif request.method == 'POST':

        entities = jsonpickle.decode(request.data)
        presences = []

        for entity in entities:
            presence = Presence()
            presence.fromJson(entity)
            try:
                presence.save()
            except Error, e:
                return e.value,e.code

            presences.append(presence.id)

        return jsonpickle.encode(presences,unpicklable=False),201

@app.route('/promotions/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/promotions/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def promotions(identifiant=None):
    if identifiant:
        promotion = Promotion()

        if request.method == 'GET':

            promotion.id = identifiant
            try:
                promotion.load()
            except Error, e:
                return e.value,e.code
            else:
                return promotion.asJson(), 200

        elif request.method == 'PUT':

            promotion.fromJson(request.data)
            try:
                promotion.save()
            except Error,e:
                return e.value,e.code
            else:
                return promotion.asJson(),201
    else:
        if request.method == 'GET':
            try:
                return jsonpickle.encode(Promotion().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
            except Error,e:
                return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            promotions = []
            for entity in entities:
                promotion = Promotion()
                promotion.fromJson(entity)
                try:
                    promotion.save()
                except Error,e:
                    return e.value,e.code

                promotions.append(promotion.id)
            return jsonpickle.encode(promotions,unpicklable=False),201

@app.route('/schedulings/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def schedulings():
    if request.method == 'GET':
        try:
            return jsonpickle.encode(Scheduling().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
        except Error, e:
            return e.value,e.code

    elif request.method == 'POST' or request.method == 'PUT':
        entities = jsonpickle.decode(request.data)
        schedulings = []
        for entity in entities:
            scheduling = Scheduling()
            scheduling.fromJson(entity)
            try:
                scheduling.save()
            except Error,e:
                return e.value,e.code

            schedulings.append(scheduling.id)
        return jsonpickle.encode(schedulings,unpicklable=False),201

@app.route('/rooms/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/rooms/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def rooms(identifiant=None):

    if identifiant:

        room = Room()
        room.id = identifiant

        if request.method == 'GET':
            try:
                room.load()
                if request.headers['Accept'].split(',')[0] == 'text/html':
                     return render_template('room.html', room = room, save = True)
            except Error, e:
                return e.value,e.code
            else:
                return room.asJson(), 200

        elif request.method == 'POST':
            if request.form :
                try:
                    room.load()
                    room.raspberry_id = request.form['rapsberry_id']
                    room.save()
                    if request.headers['Accept'].split(',')[0] == 'text/html':
                         return render_template('room.html', room = room)
                except Error, e:
                    return e.value,e.code
                else:
                    return room.asJson(), 200

    else :
        if request.method == 'GET':
            if request.headers['Accept'].split(',')[0] == 'text/html':
                rooms = Room().search()
                return render_template('rooms.html', rooms = rooms)
            else:
                try:
                    return jsonpickle.encode(Room().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
                except Error,e:
                    return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            rooms = []
            for entity in entities:
                room = Room()
                room.fromJson(entity)
                try:
                    room.save()
                except Error,e:
                    return e.value,e.code

                rooms.append(room.id)
            return jsonpickle.encode(rooms,unpicklable=False),201

# set the secret key.  keep this really secret:
app.secret_key = 'C7PZnXhzuRC7Tf3L'

if __name__ == "__main__":
    cfg = ConfigParser.ConfigParser()
    cfg.read('conf.ini')

    app.debug = cfg.get('Server','debug')

    app.run(host = cfg.get('Server','hostIP') + ':' + cfg.get('Server','port'))
