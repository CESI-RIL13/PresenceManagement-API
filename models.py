#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from __future__ import unicode_literals
from config import connexion, curseur
from datetime import datetime
import calendar
import jsonpickle
import MySQLdb #http://www.mikusa.com/python-mysql-docs/index.html
from jsonpickle import handlers
from passlib.apps import custom_app_context as pwd_context
import pyqrcode
import ConfigParser


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

        curseur.execute("SHOW COLUMNS FROM " + self.getTable())

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

    def getEntity(self, entityName):

        clzz = globals()[entityName.title()]
        entity = clzz()
        entity.id = getattr(self, entityName + '_id')

        if entity.load():
            return entity
        else:
            return False

    def load(self):

        if self.id == None or self.id == "":
            raise Error(400,"No id providing to manage the request")

        try:
            curseur.execute("SELECT * FROM " + self.getTable() +" WHERE id='%s'"%self.id)

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
        args = self._cleanArgs(args.copy())
        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if(len(where)>0):
            request += " WHERE " + " AND ".join(where)

        return self._executeSearch(request)

    def save(self):
        values = []

        for column in self.getColumns():
            if getattr(self, column) == None or column == "updated" or self.getColumns().count(column) == 0:
                continue

            if column == "password":
                setattr(self, column, User.hash_password(getattr(self, column)))

            values.append(column + " = '" + MySQLdb.escape_string(str(getattr(self, column))) + "'")

            if self.__table == 'user':
                img = pyqrcode.create(self.id)
                img.png(self.fullname, scale=8)
                values.append("qrcode = '" + img.encode("base64") + "'")

        request = "INSERT INTO " + self.getTable() + " SET " + ",".join(values) + " ON DUPLICATE KEY UPDATE " + ",".join(values)
        #print request

        try :
            if curseur.execute(request) and curseur.lastrowid:
                setattr(self,"id",curseur.lastrowid)

            for domain in self.getHasMany():
                subEntity = getattr(__import__('models'),domain.title())()

                if subEntity.getHasMany().count(self.getTable()) == 0:
                    continue

                if self.__dict__.get(domain+'_id'):
                    jointure = "%s_has_%s" % (self.getTable(),domain)

                    if(self._checkTable(jointure) == False):
                        jointure = "%s_has_%s" % (domain,self.getTable())

                    curseur.execute("INSERT INTO %s SET %s = '%s', %s = '%s' ON DUPLICATE KEY UPDATE SET %s = '%s', %s = '%s'" % (jointure,self.getTable()+"_id",self.id,domain+"_id",getattr(self,domain+"_id"),self.getTable()+"_id",self.id,domain+"_id",getattr(self,domain+"_id")))

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

        for attr in obj:
           setattr(self,attr,obj[attr])

    def asJson(self):
        return jsonpickle.encode(self, unpicklable=False)

    def __getstate__(self):
        entity = {}
        for column in self.getColumns():
            entity[column] = getattr(self,column)
        return entity

    def __setstate__(self,states):
        print "ok"

    def _checkTable(self,tableName):
        cfg = ConfigParser.ConfigParser()
        cfg.read('conf.ini')
        curseur.execute("SHOW TABLES FROM " + cfg.get('SQL','database') + " WHERE Tables_in_" + cfg.get('SQL','database') + " = '%s'"%tableName)
        return curseur.rowcount > 0

    def _constructSelect(self):
        joinClause = self._getJoinClause(self)
        request = "SELECT DISTINCT %s.id FROM %s"% (self.getTable(),self.getTable())
        return request + "".join(joinClause)

    def _constructWhereClause(self,args = {},lastUpdate = None):
        where = []

        for key in args.keys():
            if self.getColumns().count(key) == 0:
                for domain in self.getHasOne():
                    entity = getattr(__import__('models'),domain.title())()
                    if entity.getColumns().count(key) == 0 or entity.getHasMany().count(self.getTable()) > 0:
                        continue
                    else:
                        subClause = args[key].split(",")
                        where.append("%s."%(entity.getTable()) + key + " IN ( '" + "' , '".join(subClause) +"' )")
                for domain in self.getHasMany():
                    subClause = args[key].split(",")
                    entity = getattr(__import__('models'),domain.title())()
                    if entity.getHasMany().count(self.getTable()) > 0:
                        jointure = "%s_has_%s" % (self.getTable(),domain)
                        if(self._checkTable(jointure) == False):
                            jointure = "%s_has_%s" % (domain,self.getTable())

                        where.append("%s."%(jointure) + key + " IN ( '" + "' , '".join(subClause) +"' )")
                    else:
                        continue
                continue

            if key == "date_start" or key == "date_end":
                subClause = []
                subClause.append(datetime.fromtimestamp(float(args[key])).strftime("%Y-%m-%d %H:%M:%S"))
            else:
                subClause = args[key].split(",")

            where.append("%s."%(self.getTable()) + key + " IN ( '" + "' , '".join(subClause) +"' )")

        if(lastUpdate != None):
            date = datetime.strptime(lastUpdate, "%d %b %Y %H:%M:%S GMT")
            where.append("%s.updated > '%s'"%(self.getTable(),date.strftime("%Y-%m-%d %H:%M:%S")))

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

        if len(rows) == 0:
            raise Error(404,"Nothing found matching the request")

        result = []
        for row in rows:
            entity = Entity(self.getTable())
            entity.id = row['id']
            entity.load()
            result.append(entity)

        return result

    def _getJoinClause(self,entity):
        joinClause = []
        if(len(entity.getHasOne()) > 0):
            for domain in entity.getHasOne():
                joinClause.append(" LEFT JOIN %s ON %s.id = %s.%s" % (domain, domain,entity.getTable(),domain+"_id"))
                subEntity = getattr(__import__('models'),domain.title())()
                joinClause.extend(self._getJoinClause(subEntity))
        if(len(entity.getHasMany()) > 0):
            for domain in entity.getHasMany():
                if(domain == self.getTable()):
                    continue
                subEntity = getattr(__import__('models'),domain.title())()
                if subEntity.getHasMany().count(entity.getTable()) > 0:
                    jointure = "%s_has_%s" % (entity.getTable(),domain)

                    if(self._checkTable(jointure) == False):
                        jointure = "%s_has_%s" % (domain,entity.getTable())

                    joinClause.append(" LEFT JOIN %s ON %s.id = %s.%s" % (jointure,entity.getTable(),jointure,entity.getTable()+"_id"))
                else:
                    joinClause.append(" LEFT JOIN %s ON %s.id = %s.%s" % (domain,entity.getTable(), domain,entity.getTable()+"_id"))

        return joinClause

    def _cleanArgs(self, args = {}):

        for key in args.keys():
            if args[key] == "":
                args.pop(key, None)
            if type(args) == 'werkzeug.datastructures.MultiDict' and len(args.getlist(key)) > 0:
                args[key] = ",".join(args.getlist(key))
        return args

class User(Entity) :

    def __init__(self):
        Entity.__init__(self,'user')
        self.setHasMany('promotion')
        self.setHasMany('presence')
        self.setHasMany('scheduling')

    def login(self,mail,password):
        if password == '' or password == None:
            return False
        try:
            curseur.execute("SELECT id, password FROM user WHERE mail = '%s'" % (mail))

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                raise Error(400,"Error processing request")
            except IndexError:
                print "MySQL Error: %s" % str(e)
                raise Error(400, "Error processing request")

        if curseur.rowcount == 0 :
            return False
        else:
            response = curseur.fetchone()
            self.id = response['id']
            self.password = response['password']
            if self.password != None and self.password != '':
                return self.verify_password(password)
            else:
                return False

    def hash_password(password):
        return pwd_context.encrypt(password)
    hash_password = staticmethod(hash_password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def getPromotion(self):
        promotion = Promotion().search(args = {'user_id':self.id})
        return promotion[0]

class Presence(Entity) :
    def __init__(self):
        Entity.__init__(self,'presence')
        self.setHasOne('user')
        self.setBelongsTo('user')

    def search(self, args = {},lastUpdate = None):
        args = self._cleanArgs(args.copy())
        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if args.keys().count('promotion_id'):
            where.append('user_has_promotion.promotion_id  IN("%s")'%( '","'.join(args['promotion_id'].split(','))))

        if args.keys().count('date_begin') > 0 and args.keys().count('date_ending') > 0:
            where.append('presence.date BETWEEN "%s" AND "%s"'%(datetime.fromtimestamp(float(args['date_begin'])).strftime("%Y-%m-%d %H:%M:%S"),datetime.fromtimestamp(float(args['date_ending'])).strftime("%Y-%m-%d %H:%M:%S")))

        elif args.keys().count('date_begin') > 0:
            where.append('presence.date > "%s"'%(datetime.fromtimestamp(float(args['date_begin'])).strftime("%Y-%m-%d %H:%M:%S")))

        elif args.keys().count('date_ending') > 0:
            where.append('presence.date < "%s"'%(datetime.fromtimestamp(float(args['date_ending'])).strftime("%Y-%m-%d %H:%M:%S")))

        return self._executeSearch(request, where)

    def _constructWhereClause(self,args = {},lastUpdate = None):
        where = []

        for key in args.keys():
            if self.getColumns().count(key) == 0:
                for domain in self.getHasOne():
                    entity = getattr(__import__('models'),domain.title())()
                    if entity.getColumns().count(key) == 0 or entity.getHasMany().count(self.getTable()) > 0:
                        continue
                    else:
                        subClause = args[key].split(",")
                        where.append("%s."%(entity.getTable()) + key + " IN ( '" + "' , '".join(subClause) +"' )")
                for domain in self.getHasMany():
                    subClause = args[key].split(",")
                    entity = getattr(__import__('models'),domain.title())()
                    if entity.getHasMany().count(self.getTable()) > 0:
                        jointure = "%s_has_%s" % (self.getTable(),domain)
                        if(self._checkTable(jointure) == False):
                            jointure = "%s_has_%s" % (domain,entity.getTable())

                        where.append("%s."%(jointure) + key + " IN ( '" + "' , '".join(subClause) +"' )")
                    else:
                        continue
                continue

            if key == "date":
                date = datetime.fromtimestamp(float(args[key])).strftime("%Y-%m-%d")
                where.append("%s.date BETWEEN '%s 00:00:00' AND '%s 23:59:59'" % (self.getTable(),date,date))
            else:
                subClause = args[key].split(",")
                where.append("%s."%(self.getTable()) + key + " IN ( '" + "' , '".join(subClause) +"' )")

        if(lastUpdate != None):
            date = datetime.strptime(lastUpdate, "%d %b %Y %H:%M:%S GMT")
            where.append("%s.updated > '%s'"%(self.getTable(),date.strftime("%Y-%m-%d %H:%M:%S")))

        return where

    def fromJson(self,json):
        if type(json) is str:
            obj = jsonpickle.decode(json)
        else:
            obj = json

        for attr in obj:
            if attr == 'date': setattr(self,attr, datetime.fromtimestamp(float(obj[attr])).strftime("%Y-%m-%d %H:%M:%S"))
            else:
                setattr(self,attr,obj[attr])

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
        args = self._cleanArgs(args.copy())
        request = self._constructSelect()
        where = self._constructWhereClause(args,lastUpdate)

        if args.keys().count('raspberry_id'):
            where.append('room.raspberry_id ="%s"'%(args['raspberry_id']))

        if args.keys().count('date'):
            date = datetime.fromtimestamp(float(args['date'])).strftime("%Y-%m-%d")
            where.append('scheduling.date_start > "%s 00:00:00" AND scheduling.date_end < "%s 23:59:59"' % (date,date))

        if args.keys().count('date_begin') > 0:
            where.append('scheduling.date_start > "%s"'%(datetime.fromtimestamp(float(args['date_begin'])).strftime("%Y-%m-%d 00:00:00")))

        if args.keys().count('date_ending') > 0:
            where.append('scheduling.date_ending < "%s"'%(datetime.fromtimestamp(float(args['date_ending'])).strftime("%Y-%m-%d 23:59:59")))

        return self._executeSearch(request, where)

    def fromJson(self,json):
        if type(json) is str:
            obj = jsonpickle.decode(json)
        else:
            obj = json

        for attr in obj:
            if attr == 'date_start' or attr == 'date_end' : setattr(self,attr, datetime.fromtimestamp(float(obj[attr])).strftime("%Y-%m-%d %H:%M:%S"))
            else:
                setattr(self,attr,obj[attr])