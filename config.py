#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
import MySQLdb #http://www.mikusa.com/python-mysql-docs/index.html
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('conf.ini')

connexion = MySQLdb.connect(host=cfg.get('SQL','hostIP'), # your host, usually localhost
                     port=int(cfg.get('SQL','port')),
                     user=cfg.get('SQL','user'), # your username
                      passwd=cfg.get('SQL','password'), # your password
                      db=cfg.get('SQL','database')) # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
curseur = connexion.cursor(MySQLdb.cursors.DictCursor)