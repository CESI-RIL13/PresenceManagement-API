#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from models import *
import jsonpickle

from config import connexion,curseur

room = Room()
room.load()
room.name = 'LACANAUX'
room.raspberry_id = 'AGIGS657DSzqdzqdqz'
room.save()
print room.id
# print user.__dict__
# print jsonpickle.encode(user, unpicklable=False)
# JSON = user.asJson()
# print JSON
#
# user2 = User()
#
# user2.fromJson(JSON)
#
# print user2.__dict__

# curseur.execute("SELECT * FROM user WHERE id='1234567890'")
# print curseur.fetchone()

# args = {}
# #args['id'] = '1234567890,befg'
# args['promotion_id'] = 'BO30440'
#
# results = Entity('user').search(args)
#
# print jsonpickle.encode(results,unpicklable=False)
