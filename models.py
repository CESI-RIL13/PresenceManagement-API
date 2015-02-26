#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from config import connexion, curseur
from datetime import datetime
import calendar
import jsonpickle
from jsonpickle import handlers


class DatetimeHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        return calendar.timegm(obj.timetuple())

handlers.registry.register(datetime, DatetimeHandler)
jsonpickle.set_encoder_options('simplejson', sort_keys=True)

class Entity(object) :

    def __init__(self,table):
        self.__table = table
        self.__columns = []
        self.loadColumns()
        for column in self.getColumns():
            setattr(self,column,None)

    def loadColumns(self):

        curseur.execute("SHOW COLUMNS FROM " + self.__table)

        if curseur.rowcount == 0 :
            return False

        columns = curseur.fetchall()
        for column in columns:
            self.__columns.append(column['Field'])

    def setColumn(self,value):
        self.__columns.append(value)

    def getColumns(self):
        return self.__columns

    def getTable(self):
        return self.__table

    def load(self):

        if self.id == None:
            return False

        curseur.execute("SELECT * FROM " + self.__table +" WHERE id='"+self.id+"'")

        if curseur.rowcount == 0 :
            return False

        datas = curseur.fetchone()

        for column in self.__columns:
            setattr(self,column,datas[column])

    def search(self, args = {}):
        if len(args) == 0:
            return False

        where = []

        request = "SELECT id FROM " + self.__table + " WHERE "
        for key in args.keys():
            if self.getColumns().count(key) == 0:
                continue
            subClause = args[key].split(",")
            where.append(key + " IN ( '" + "' , '".join(subClause) +"' )")

        request += " AND ".join(where)
        print request
        curseur.execute(request)
        rows = curseur.fetchall()

        result = []
        for row in rows:
            entity = Entity(self.__table)
            entity.id = row['id']
            entity.load()
            result.append(entity)

        return result



    def save(self):
        if self.id == None:
            return False

        values = []

        for column in self.__columns:
            values.append(column)

    def __getstate__(self):
        entity = {}
        for column in self.getColumns():
            entity[column] = getattr(self,column)
        return entity

    @staticmethod
    def fromDb(obj,table):
        e = Entity(table)
        for key in e.__dict__.keys():
            setattr(e, key, obj[key])
        return e

    def fromJson(self,json):
        obj = jsonpickle.decode(json)
        for key in self.getColumns():
            if key == 'updated': setattr(self, key, datetime.fromtimestamp(obj[key]))
            else: setattr(self, key, obj[key])

    def asJson(self):
        print self.__dict__
        return jsonpickle.encode(self, unpicklable=False)

    # def __str__(self):
    #     return '{' + str(self.id) + '} ' + self.name + ' ' + self.email + ' ' + str(self.updated)

class User(Entity) :

    def __init__(self):
        Entity.__init__(self,'user')

class Presence(object) :
    def __init__(self):
        Entity.__init__(self,'presence')

class Room(object) :
    def __init__(self):
        Entity.__init__(self,'room')

class Promotion(object) :
    def __init__(self):
        Entity.__init__(self,'promotion')

class Scheduling(object) :
    def __init__(self):
        Entity.__init__(self,'scheduling')