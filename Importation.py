#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cedric'
import copy
import csv
import configparser
import unicodedata
from models import *
from time import mktime

class Importation:
    def __init__(self, nomFichier):
        self.nomFichier=nomFichier
        self.configuration=configparser.RawConfigParser()
        self.configuration.read("lectureExport.cfg")
        self.adresseServeur=self.configuration.get("autres","adresseserveur")
        self.data=[]

    def remove_accents(input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    remove_accents=staticmethod(remove_accents)

    def getNomConfig(config, value, section = "nomChamps"):
        # config=configparser.RawConfigParser()
        for item in config.items(section):
            if item[1] == value:
                return item[0]
        return None
    getNomConfig=staticmethod(getNomConfig)

    def mappageConfig(nomConfig, map):
        return map[nomConfig] if nomConfig in map else -1
    mappageConfig=staticmethod(mappageConfig)

    def isPresent(tab,name):
        for liste in tab:
            if liste["name"] == name:
                return True
        return False
    isPresent=staticmethod(isPresent)

    def importerCsv(self):
        cr = csv.reader(open(self.nomFichier,"rb"))
        map={}
        pos={}
        champsImportes={}
        promo=0
        for row in cr:
            if pos == {}:
                if len(row) > 1:
                    index=0
                    for nomChamps in row:
                        nomChamps = nomChamps
                        if Importation.getNomConfig(self.configuration,nomChamps) <> None:
                            map[Importation.getNomConfig(self.configuration,nomChamps)]=index
                        index+=1
                    pos["user.id"]=Importation.mappageConfig("user.id",map)
                    pos["user.name"]=Importation.mappageConfig("user.name",map)
                    pos["user.firstname"]= Importation.mappageConfig("user.firstname",map)
                    pos["user.mail"]= Importation.mappageConfig("user.mail",map)
                    pos["user.promotion_id"]=Importation.mappageConfig("user.promotion_id",map)
                    pos["promotion.id"]=Importation.mappageConfig("promotion.id",map)
                    pos["promotion.name"]= Importation.mappageConfig("promotion.name",map)
                    pos["room.name"]=Importation.mappageConfig("room.name",map)
                    pos["scheduling.date"] =Importation.mappageConfig("scheduling.date",map)
                    pos["scheduling.heure"]=Importation.mappageConfig("scheduling.heure",map)
                    pos["scheduling.room_name"]=Importation.mappageConfig("scheduling.room_name",map)
                    pos["scheduling.promotion_id"]=Importation.mappageConfig("scheduling.promotion_id",map)
                    pos["scheduling.user_name"]=Importation.mappageConfig("scheduling.user_name",map)
                    pos["scheduling.course"]=Importation.mappageConfig("scheduling.course", map)
                else:
                    promo=row[0]
            else:
                for clef,valeur in pos.items():
                    if valeur <> -1:
                        champsImportes[clef]="%s"%(row[valeur])
                if promo <> 0:
                    champsImportes["scheduling.promotion_id"]=promo
                # print champsImportes
                self.data.append(copy.copy(champsImportes))
                champsImportes.clear()

    def importRooms(self):
        tabRooms=[]
        tabRoomsExistantes=[]
        for scheduling in self.data:
            if not Importation.isPresent(tabRooms, scheduling["scheduling.room_name"]) and not Importation.isPresent(tabRoomsExistantes,scheduling["scheduling.room_name"]):
                room=Room()
                try:
                    room.search({"name" : scheduling["scheduling.room_name"]})
                    tabRoomsExistantes.append({"name" : scheduling["scheduling.room_name"], "add" : False})
                except Error,e:
                    if e.code == 404:
                        tabRooms.append({"name" : scheduling["scheduling.room_name"]})

        print(tabRooms)
        return jsonpickle.encode(tabRooms)

    def importSchedulings(self):
        schedulings=[]
        rooms={}
        users={}
        room=Room()
        user=User()
        for planning in self.data:
            # planning={}
            scheduling={}
            planning["scheduling.date"]=str(planning["scheduling.date"]).split('. ')[1]
            # print planning["scheduling.date"]
            heures=str(planning["scheduling.heure"]).split(" / ")
            # print heures

            from_dateStart=planning["scheduling.date"]+ " " + heures[0]
            scheduling["date_start"] = str(mktime(datetime.strptime(from_dateStart,"%d/%m/%y %H:%M").timetuple()))
            from_dateEnd=planning["scheduling.date"] + " " + heures[1]
            scheduling["date_end"]= str(mktime(datetime.strptime(from_dateEnd,"%d/%m/%y %H:%M").timetuple()))

            if not planning["scheduling.room_name"] in rooms:
                entity = room.search({"name" : planning["scheduling.room_name"]})
                rooms[planning["scheduling.room_name"]]= entity[0].id
            scheduling["room_id"]=str(rooms[planning["scheduling.room_name"]])

            if 'scheduling.user_name' in planning.keys():
                if not planning["scheduling.user_name"] in users:
                    entity = user.search({"fullname" : planning["scheduling.user_name"]})
                    users[planning["scheduling.user_name"]]= entity[0].id
                scheduling["user_id"]=users[planning["scheduling.user_name"]]

            scheduling["promotion_id"]=planning["scheduling.promotion_id"]

            if planning.has_key("scheduling.course"):
                scheduling["course"] = planning["scheduling.course"]

            schedulings.append(scheduling)

        print(schedulings)
        return jsonpickle.encode(schedulings)

    def importPromo(self):
        tabPromo=[]
        for utilisateur in self.data:
            promotion = Promotion()
            promotion.id = utilisateur["user.promotion_id"]
            try:
                promotion.load()
            except Error, e:
                if e.code == 404:
                    name=str(utilisateur["promotion.name"]).split(" ")
                    # print(name)
                    tabPromo.append({"id" : utilisateur["user.promotion_id"], "name" : name[0] + name[1]})
                    # print(tabPromo)

        return jsonpickle.encode(tabPromo)

    def importUsers(self):
        users=[]
        for utilisateur in self.data:
            # utilisateur={}
            user={}
            # print(utilisateur)
            utilisateur["user.fullname"] = utilisateur["user.firstname"] + " " + utilisateur["user.name"]
            utilisateur["user.role"]="stagiaire"
            del utilisateur["user.name"]
            del utilisateur["user.firstname"]
            # print(utilisateur)
            for clef,valeur in utilisateur.items():
                key=str(clef).split('.')
                if key[0] == "user":
                    user[key[1]]=valeur
            # print user
            users.append(user)
        return jsonpickle.encode(users)