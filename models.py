#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from config import connexion, curseur

class Entity(object) :

    def __init__(self,table):
        self.__table = table
        self.__columns = []
        self.__hasOne = []
        self.__hasMany = []
        self.__belongsTo = []

        self.loadColumns()

    def loadColumns(self):

        curseur.execute("SHOW COLUMNS FROM " + self.__table)

        if curseur.rowcount == 0 :
            return False

        columns = curseur.fetchall()
        for column in columns:
            self.__columns.append(column[0])

    def setColumn(self,value):
        self.__columns.append(value)

    def getColumns(self):
        return self.__columns

    def getTable(self):
        return self.__table

    def setHasMany(self,value):
        self.__hasMany.append(value)

    def setHasOne(self,value):
        self.__hasOne.append(value)

    def setBelongsTo(self,value):
        self.__belongsTo.append(value)

    def load(self):
        if self.id == None:
            return False

        curseur.execute("SELECT * FROM " + self.__table +" WHERE id='"+self.id+"'")

        if curseur.rowcount == 0 :
            return False

        datas = curseur.fetchone()

        for column in self.__columns:
            if(len(self.__hasOne) > 0 and column.find('_id') > -1 and self.__hasOne.count(column[:column.index('_')])):
                entity = Entity(column[:column.index('_')])
                entity.id = datas[self.__columns.index(column)]
                entity.load()
                setattr(self,column,entity)
            else :
                setattr(self,column,datas[self.__columns.index(column)])

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

    def __setstate__(self,states):
        print states
        print "ok"

class User(Entity) :

    def __init__(self):
        Entity.__init__(self,'user')
        for column in self.getColumns():
            setattr(self,column,None)
        self.setHasOne('promotion')

class Presence(object) :
    def __init__(self):
        return

class Room(object) :
    def __init__(self):
        return

class Promotion(object) :
    def __init__(self):
        Entity.__init__(self,'promotion')
        for column in self.getColumns():
            setattr(self,column,None)
        return

class Scheduling(object) :
    def __init__(self):
        return