#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
import MySQLdb #http://www.mikusa.com/python-mysql-docs/index.html

connexion = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="presence_management") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
curseur = connexion.cursor()