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
    return 'hello'

@app.route('/users/')
@app.route('/users/<identifiant>')
def users(identifiant=None):
    if identifiant:
        user = User()
        user.id = identifiant
        user.load()
        return user.asJson()
    else :
        return jsonpickle.encode(User().search(request.args),unpicklable=False)


@app.route('/presences/')
@app.route('/presences/<identifiant>')
def presences(identifiant = None):
    if identifiant:
        return jsonpickle.encode(Presence().search(request.args),unpicklable=False)
    else :
        curseur.execute('SELECT id FROM presence')
        rows = curseur.fetchall()
        liste_users = []

        for row in rows:
            user = User()
            user.id = row['user_id']
            user.load()
            liste_users.append(user)

        return jsonpickle.encode(liste_users,unpicklable=False)


if __name__ == "__main__":
    app.debug = True
    app.run()