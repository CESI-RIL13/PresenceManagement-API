#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from flask import Flask
from config import connexion, curseur

app = Flask(__name__)

@app.route("/")
def hello():
    return 'hello'

if __name__ == "__main__":
    app.debug = True
    app.run()