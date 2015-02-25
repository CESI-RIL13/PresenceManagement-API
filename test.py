#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import connexion, curseur
__author__ = 'Dos Santos Julien'

curseur.execute("SELECT * FROM user WHERE id='1234567890'")

if curseur.rowcount == 0 :
    print 0

infos =  curseur.fetchone()

print infos

print infos[0]
print infos[1]