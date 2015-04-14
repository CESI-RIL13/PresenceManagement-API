#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'Dos Santos Julien'
from flask import *
from models import *
import jsonpickle
import ConfigParser
import os
from Importation import *
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/tmp/'
ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def detect_user_login():

    if not request.headers['Accept'].split(',')[0] == 'text/html':
        return

    if request.endpoint == 'static':
        return

    if not 'user_id' in session and request.endpoint != 'login':
        return redirect(url_for('login'))

    if 'user_id' in session and request.endpoint == 'login':
        return redirect(url_for('hello'))

@app.before_request
def detect_auth_client():
    if request.headers['Accept'].split(',')[0] == 'text/html':
        return

    if request.endpoint == 'static':
        return

    if (not request.headers.get('X-API-Client-Auth') or not Room().authentification(request.headers.get('X-API-Client-Auth'))) and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.before_request
def connect_db():
    # cfg = ConfigParser.ConfigParser()
    # cfg.read('conf.ini')
    #
    # connexion = MySQLdb.connect(host=cfg.get('SQL','hostIP'), # your host, usually localhost
    #                             port=int(cfg.get('SQL','port')),
    #                             user=cfg.get('SQL','user'), # your username
    #                             passwd=cfg.get('SQL','password'), # your password
    #                             db=cfg.get('SQL','database'),
    #                             charset='utf8') # name of the data base
    #
    # # you must create a Cursor object. It will let
    # #  you execute all the queries you need
    # curseur = connexion.cursor(MySQLdb.cursors.DictCursor)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    # print datetime.strptime(request.headers.get('If-Modified-Since'), "%d %b %Y %H:%M:%S GMT")

    user = User()
    user.id = session['user_id']
    user.load()

    if request.headers['Accept'].split(',')[0] == 'text/html':
        return redirect(url_for('presences'))
    else:
        return 'Circulez y a rien à voir !'

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.headers['Accept'].split(',')[0] == 'text/html':

        if request.method == 'GET':
            return render_template('index.html')

        if request.method == 'POST':
            user = User()
            if user.login(request.form['mail'],request.form['password']):
                session['user_id'] = user.id
                return redirect(url_for('presences'))
            else:
                if request.headers['Accept'].split(',')[0] == 'text/html':
                    flash('Informations de connexion incorect','error')
                    return redirect(url_for('login'))
                else:
                    return "Invalid password",401

    else:
        return 'logue toi !',401

@app.route('/logout/', methods = ['GET'])
def logout():
    if request.headers['Accept'].split(',')[0] == 'text/html':

        if request.method == 'GET' and 'user_id' in session:
            del session['user_id']
            flash('Vous avez été déconnecté avec succès','success')

        return redirect(url_for('login'))

@app.route('/users/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/users/<identifiant>', methods = ['GET', 'PUT', 'DELETE'])
def users(identifiant=None):
    if identifiant:

        user = User()

        if request.method == 'GET':
            user.id = identifiant

            try:
                user.load()

            except Error, e:
                return e.value, e.code
            else:
                if request.headers['Accept'].split(',')[0] == 'text/html':
                    if user.role == 'stagiaire' or user.role == 'intervenant':
                        return render_template('participant.html', user = user)
                    else:
                        return render_template('utilisateur.html', user = user)
                else:
                    return user.asJson(),200

        elif request.method == 'PUT':
            user.fromJson(request.data)
            try :
                user.save()

            except Error, e:
                return e.value,e.code
            else:
                return user.asJson(),201
    else :

        if request.method == 'GET':
            if request.headers['Accept'].split(',')[0] == 'text/html':
                try:
                    users = User().search(request.args,request.headers.get('If-Modified-Since'))
                    return render_template('utilisateurs.html', users = users)
                except Error, e:
                   return render_template('utilisateurs.html')

            else:
                try:
                    return jsonpickle.encode(User().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
                except Error, e:
                    return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':

            entities = jsonpickle.decode(request.data)
            users = []
            for entity in entities:
                user = User()
                user.fromJson(entity)
                try:
                    user.save()
                except Error, e:
                    return e.value,e.code

                users.append(user.id)
            return jsonpickle.encode(users,unpicklable=False),201

@app.route('/presences/', methods = ['GET', 'POST'])
def presences():
    if request.method == 'GET':
        if request.headers['Accept'].split(',')[0] == 'text/html':
            presences = []
            promotions = []

            try:
                promotions = Promotion().search()
                presences = Presence().search(request.args)
                return render_template('presences.html', presences = presences, promotions = promotions)
            except Error, e:
                print e
                presences = False
            finally:
                return render_template('presences.html', presences = presences, promotions = promotions)

        else:
            try:
                return jsonpickle.encode(Presence().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
            except Error, e:
                return e.value,e.code

    elif request.method == 'POST':

        entities = jsonpickle.decode(request.data)
        presences = []

        for entity in entities:
            presence = Presence()
            presence.fromJson(entity)
            try:
                presence.save()
            except Error, e:
                return e.value,e.code

            presences.append(presence.id)

        return jsonpickle.encode(presences,unpicklable=False),201

@app.route('/promotions/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/promotions/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def promotions(identifiant=None):
    if identifiant:
        promotion = Promotion()

        if request.method == 'GET':

            promotion.id = identifiant
            try:
                promotion.load()
            except Error, e:
                return e.value,e.code
            else:
                return promotion.asJson(), 200

        elif request.method == 'PUT':

            promotion.fromJson(request.data)
            try:
                promotion.save()
            except Error,e:
                return e.value,e.code
            else:
                return promotion.asJson(),201
    else:
        if request.method == 'GET':
            try:
                return jsonpickle.encode(Promotion().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
            except Error,e:
                return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            promotions = []
            for entity in entities:
                promotion = Promotion()
                promotion.fromJson(entity)
                try:
                    promotion.save()
                except Error,e:
                    return e.value,e.code

                promotions.append(promotion.id)
            return jsonpickle.encode(promotions,unpicklable=False),201

@app.route('/schedulings/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def schedulings():
    if request.method == 'GET':
        try:
            return jsonpickle.encode(Scheduling().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
        except Error, e:
            return e.value,e.code

    elif request.method == 'POST' or request.method == 'PUT':
        entities = jsonpickle.decode(request.data)
        schedulings = []
        for entity in entities:
            scheduling = Scheduling()
            scheduling.fromJson(entity)
            try:
                scheduling.save()
            except Error,e:
                return e.value,e.code

            schedulings.append(scheduling.id)
        return jsonpickle.encode(schedulings,unpicklable=False),201

@app.route('/rooms/', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/rooms/<identifiant>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def rooms(identifiant=None):

    if identifiant:

        room = Room()
        room.id = identifiant

        if request.method == 'GET':
            try:
                room.load()
                if request.headers['Accept'].split(',')[0] == 'text/html':
                     return render_template('room.html', room = room, save = True)
                else:
                    return room.asJson(), 200
            except Error, e:
                return e.value,e.code


        elif request.method == 'POST':
            room.load()
            if request.form['rapsberry_id'] :
                try:
                    room.raspberry_id = request.form['rapsberry_id']
                    room.save()
                    if request.headers['Accept'].split(',')[0] == 'text/html':
                         return render_template('room.html', room = room, success = True)
                    else:
                        return room.asJson(), 200
                except Error, e:
                    return e.value,e.code

            else :
                return render_template('room.html', room = room, error = True)

    else :
        if request.method == 'GET':
            if request.headers['Accept'].split(',')[0] == 'text/html':
                rooms = Room().search()
                return render_template('rooms.html', rooms = rooms)
            else:
                try:
                    return jsonpickle.encode(Room().search(request.args,request.headers.get('If-Modified-Since')),unpicklable=False),200
                except Error,e:
                    return e.value,e.code

        elif request.method == 'POST' or request.method == 'PUT':
            entities = jsonpickle.decode(request.data)
            rooms = []
            for entity in entities:
                room = Room()
                room.fromJson(entity)
                try:
                    room.save()
                except Error,e:
                    return e.value,e.code

                rooms.append(room.id)
            return jsonpickle.encode(rooms,unpicklable=False),201

@app.route('/imports/', methods = ['GET','POST','PUT'])
@app.route('/imports/<type>', methods = ['POST', 'PUT'])
def imports(type=None):

    if request.method == 'GET' and request.headers['Accept'].split(',')[0] == 'text/html':
        return render_template('imports.html')

    elif request.method == 'POST' or request.method == 'PUT':

        if not type and request.form['type']:
            type = request.form['type']
        else :
            if request.headers['Accept'].split(',')[0] == 'text/html':
                flash('Choisissez un type d\'importation','error')
                return redirect(url_for('imports'),400)
            else:
                return "Specified type of the import",400

        file = request.files['file']

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            importation = Importation(app.config['UPLOAD_FOLDER'] + filename)

            try :
                if(type=="users"):

                    importation.importerCsv()
                    try:
                        promos = jsonpickle.decode(importation.importPromo())
                    except ImportationError:
                        if request.headers['Accept'].split(',')[0] == 'text/html':
                            flash('Mauvais type de fichier','error')
                            return redirect(url_for('imports'),400)
                        else:
                            return "Mauvais type de fichier",400

                    if len(promos) > 0:
                        for entity in promos:
                            promo = Promotion()
                            promo.fromJson(entity)
                            try:
                                promo.save()
                            except Error, e:
                                if request.headers['Accept'].split(',')[0] == 'text/html':
                                    flash(e.value,'error')
                                    return redirect(url_for('imports'),400)
                                else:
                                    return e.value,e.code
                    try:
                        entities = jsonpickle.decode(importation.importUsers())
                    except ImportationError:
                        if request.headers['Accept'].split(',')[0] == 'text/html':
                            flash('Mauvais type de fichier','error')
                            return redirect(url_for('imports'),400)
                        else:
                            return "Mauvais type de fichier",400

                    users = []
                    for entity in entities:
                        user = User()
                        user.fromJson(entity)
                        try:
                            user.save()
                        except Error, e:
                            if request.headers['Accept'].split(',')[0] == 'text/html':
                                flash(e.value,'error')
                                return redirect(url_for('imports'),400)
                            else:
                                return e.value,e.code

                        users.append(user.id)
                    if request.headers['Accept'].split(',')[0] == 'text/html':
                        flash(str(len(users)) + ' utilisateurs ont été importé','success')
                        return redirect(url_for('imports'),201)
                    else:
                        return jsonpickle.encode(users,unpicklable=False),201

                elif(type=="schedulings"):
                    importation.importerCsv()

                    try:
                        rooms = jsonpickle.decode(importation.importRooms())
                    except ImportationError,e:
                        print e
                        if request.headers['Accept'].split(',')[0] == 'text/html':
                            flash('Mauvais type de fichier','error')
                            return redirect(url_for('imports')),400
                        else:
                            return "Mauvais type de fichier",400

                    if len(rooms) > 0:
                        for entity in rooms:
                            room = Room()
                            room.fromJson(entity)
                            try:
                                room.save()
                            except Error, e:
                                if request.headers['Accept'].split(',')[0] == 'text/html':
                                    flash(e.value,'error')
                                    return redirect(url_for('imports')),400
                                else:
                                    return e.value,e.code
                    try:
                        entities = jsonpickle.decode(importation.importSchedulings())
                    except ImportationError, e:
                        print e
                        if request.headers['Accept'].split(',')[0] == 'text/html':
                            flash('Mauvais type de fichier','error')
                            return redirect(url_for('imports')),400
                        else:
                            return "Mauvais type de fichier",400

                    schedulings = []
                    for entity in entities:
                        scheduling = Scheduling()
                        scheduling.fromJson(entity)
                        try:
                            scheduling.save()
                        except Error, e:
                            if request.headers['Accept'].split(',')[0] == 'text/html':
                                flash(e.value,'error')
                                return redirect(url_for('imports')),400
                            else:
                                return e.value,e.code

                        schedulings.append(scheduling.id)

                    if request.headers['Accept'].split(',')[0] == 'text/html':
                        flash(str(len(schedulings)) + ' planning ont été importé','success')
                        return redirect(url_for('imports'),201)
                    else:
                        return jsonpickle.encode(schedulings,unpicklable=False),201
                    #return 'test',200

            except Error, e:
                return e.value, e.code

        else:
            if request.headers['Accept'].split(',')[0] == 'text/html':
                flash('Aucun fichier, fournir un fichier CSV','error')
                return redirect(url_for('imports')),400
            else:
                return "Not file provided, please provide a CSV file",400

    else:
        return 405

# set the secret key.  keep this really secret:
app.secret_key = 'C7PZnXhzuRC7Tf3L'

if __name__ == "__main__":
    cfg = ConfigParser.ConfigParser()
    cfg.read('conf.ini')

    app.debug = cfg.get('Server','debug')

    app.run(host = cfg.get('Server','hostIP'), port=int(cfg.get('Server','port')))
