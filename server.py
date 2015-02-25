#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from flask import Flask
from config import connexion, curseur
from models import User
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
        return jsonpickle.encode(user,unpicklable=False)
    else :
        curseur.execute('SELECT * FROM user')
        rows = curseur.fetchall()
        liste_users = []

        for row in rows:
            user = User()
            user.id = row[0]
            user.load()
            liste_users.append(user)

        return jsonpickle.encode(liste_users,unpicklable=False)


if __name__ == "__main__":
    app.debug = True
    app.run()