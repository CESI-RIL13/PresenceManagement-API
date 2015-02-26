#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from models import Entity, User
import jsonpickle

from config import connexion,curseur

# user = User()
# user.id = '1234567890'
# user.load()
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

args = {}
#args['id'] = '1234567890,befg'
args['promotion_id'] = 'BO30440'

results = Entity('user').search(args)

print jsonpickle.encode(results,unpicklable=False)
