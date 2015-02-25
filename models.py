#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from config import connexion, curseur
class User(object) :

    def __init__(self):
        self.id = 0
        self.name = ""
        self.firstname = ""
        self.mail = ""
        self.promotion_id = ""
        self.updated = ""
        return

    def load(self):

        if self.id == 0:
            return False

        curseur.execute("SELECT * FROM user WHERE id="+self.id)

        if curseur.rowcount == 0 :
            return False

        infos = curseur.fetchone()
        self.name = infos[1]
        self.firstname = infos[2]
        self.mail = infos[3]
        self.promotion_id = infos[4]
        self.updated = infos[5]

        return True

class Presence(object) :
    def __init__(self):
        return

class Room(object) :
    def __init__(self):
        return

class Promotion(object) :
    def __init__(self):
        return

class Scheduling(object) :
    def __init__(self):
        return