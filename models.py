#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from config import connexion, curseur
from datetime import datetime
import calendar
import jsonpickle
import MySQLdb #http://www.mikusa.com/python-mysql-docs/index.html
from jsonpickle import handlers


class DatetimeHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        return calendar.timegm(obj.timetuple())

handlers.registry.register(datetime, DatetimeHandler)
jsonpickle.set_encoder_options('simplejson', sort_keys=True)

class Error(Exception):
     def __init__(self, code, value):
        self.value = value
        self.code = code

     def __str__(self):
         return repr(self.value)

class Entity(object) :

    def __init__(self,table):
        self.__table = table
        self.__columns = []
        self.__hasOne = []
        self.__hasMany = []
        self.__belongsTo = []
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

    def setColumn(self,value):
        self.__columns.append(value)

    def getColumns(self):
        return self.__columns

    def getTable(self):
        return self.__table

    def setHasMany(self,value):
        self.__hasMany.append(value)

    def getHasMany(self):
        return self.__hasMany

    def setHasOne(self,value):
        self.__hasOne.append(value)

    def getHasOne(self):
        return self.__hasOne

    def setBelongsTo(self,value):
        self.__belongsTo.append(value)

    def load(self):

        if self.id == None or self.id == "":
            raise Error(400,"No id providing to manage the request")

        try:
            curseur.execute("SELECT * FROM " + self.__table +" WHERE id='%s'"%self.id)

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                raise Error(400,"Error processing request")
            except IndexError:
                print "MySQL Error: %s" % str(e)
                raise Error(400, "Error processing request")

        if curseur.rowcount == 0 :
            raise Error(404,"Nothing found matching the request")

        datas = curseur.fetchone()

        for column in self.__columns:

            # if(len(self.__hasOne) > 0 and column.find('_id') > -1 and self.__hasOne.count(column[:column.index('_')])):
            #     entity = Entity(column[:column.index('_')])
            #     entity.id = datas[column]
            #     entity.load()
            #     setattr(self,column,entity)
            # else :
                setattr(self,column,datas[column])

        return True

    def search(self, args = {},lastUpdate = None):

        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if(len(where)>0):
            request += " WHERE " + " AND ".join(where)

        return self._executeSearch(request)

    def save(self):
        values = []

        for column in self.__columns:
            if getattr(self, column) == None or column == "updated":
                continue
            if type(getattr(self, column)) is datetime:
                values.append(column + " = '" + MySQLdb.escape_string(getattr(self, column).strftime("%Y-%m-%d %H:%M:%S")) + "'")
            else:
                values.append(column + " = '" + MySQLdb.escape_string(getattr(self, column)) + "'")


        request = "INSERT INTO " + self.__table + " SET " + ",".join(values) + " ON DUPLICATE KEY UPDATE " + ",".join(values)

        try :
            if curseur.execute(request) and curseur.lastrowid:
                setattr(self,"id",curseur.lastrowid)

            connexion.commit()
            return True

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                raise Error(400,"Error occuring processing the request")
            except IndexError:
                print "MySQL Error: %s" % str(e)
                raise Error(400,"Error occuring processing the request")

    def fromDb(obj,table):
        e = Entity(table)
        for key in e.__dict__.keys():
            setattr(e, key, obj[key])
        return e

    def fromJson(self,json):
        if type(json) is str:
            obj = jsonpickle.decode(json)
        else:
            obj = json

        for key in self.getColumns():
            if obj.get(key) == None:
                continue
            if key == 'updated': setattr(self, key, datetime.fromtimestamp(obj[key]))
            else: setattr(self, key, obj[key])

    def asJson(self):
        return jsonpickle.encode(self, unpicklable=False)

    # def __str__(self):
    #     return '{' + str(self.id) + '} ' + self.name + ' ' + self.email + ' ' + str(self.updated)

    def __getstate__(self):
        entity = {}
        for column in self.getColumns():
            entity[column] = getattr(self,column)
        return entity

    def __setstate__(self,states):
        print "ok"

    def _constructSelect(self):
        joinClause = Entity.__getJoinClause(self)
        request = "SELECT %s.id FROM %s"% (self.__table,self.__table)
        return request + "".join(joinClause)

    def _constructWhereClause(self,args = {},lastUpdate = None):
        where = []

        for key in args.keys():
            if self.getColumns().count(key) == 0:
                # for domain in self.getHasOne():
                #     entity = getattr(__import__('models'),domain.title())()
                #     if entity.getColumns().count(key) == 0 or entity.getHasMany().count(self.__table) > 0:
                #         continue
                #     else:
                #         subClause = args[key].split(",")
                #         where.append("%s."%(entity.__table) + key + " IN ( '" + "' , '".join(subClause) +"' )")
                continue

            subClause = args[key].split(",")
            where.append("%s."%(self.__table) + key + " IN ( '" + "' , '".join(subClause) +"' )")

        if(lastUpdate != None):
            date = datetime.strptime(lastUpdate, "%d %b %Y %H:%M:%S GMT")
            where.append("%s.updated > '%s'"%(self.__table,date.strftime("%Y-%m-%d %H:%M:%S")))

        return where

    def _executeSearch(self,request = None,where = []):

        if request == None:
            return False

        if len(where)>0:
            request += " WHERE " + " AND ".join(where)

        print request

        try:
            curseur.execute(request)

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
                raise Error(400,"Error occuring processing the request")

        rows = curseur.fetchall()

        result = []
        for row in rows:
            entity = Entity(self.__table)
            entity.id = row['id']
            entity.load()
            result.append(entity)

        return result

    def __getJoinClause(entity):
        joinClause = []
        if(len(entity.getHasOne()) > 0):
            for domain in entity.getHasOne():
                joinClause.append(" JOIN %s ON %s.id = %s.%s" % (domain, domain,entity.getTable(),domain+"_id"))
                subEntity = getattr(__import__('models'),domain.title())()
                joinClause.extend(Entity.__getJoinClause(subEntity))
        return joinClause

class User(Entity) :
    def __init__(self):
        Entity.__init__(self,'user')
        self.setHasOne('promotion')
        self.setHasMany('presence')
        self.setHasMany('scheduling')

class Presence(Entity) :
    def __init__(self):
        Entity.__init__(self,'presence')
        self.setHasOne('user')
        self.setBelongsTo('user')

    def search(self, args = {},lastUpdate = None):
        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if args.keys().count('promotion_id'):
            where.append('promotion.id ="%s"'%(args['promotion_id']))

        return self._executeSearch(request, where)

class Room(Entity) :
    def __init__(self):
        Entity.__init__(self,'room')
        self.setHasMany('scheduling')

class Promotion(Entity) :
    def __init__(self):
        Entity.__init__(self,'promotion')
        self.setHasMany('scheduling')
        self.setHasMany('user')

class Scheduling(Entity) :
    def __init__(self):
        Entity.__init__(self,'scheduling')
        self.setHasOne('room')
        self.setHasOne('promotion')
        self.setBelongsTo('promotion')

    def search(self, args = {},lastUpdate = None):
        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if args.keys().count('raspberry_id'):
            where.append('room.raspberry_id ="%s"'%(args['raspberry_id']))

        return self._executeSearch(request, where)