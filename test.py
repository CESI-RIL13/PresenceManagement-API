#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from models import Entity, User
import jsonpickle

user = User()
user.id = '1234567890'
user.load()
JSON = jsonpickle.encode(user)
print JSON

user = jsonpickle.decode(JSON)

print user