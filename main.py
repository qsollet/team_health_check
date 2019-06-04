from flask import Flask, render_template, send_from_directory, session, request
import random
import json
import uuid
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aifk9042wkjefkj29e0fpowekjf!'

# rooms = {room_id: {uuid_1: {name: 'my name', vote: 'A'}, uuid_2: {name: 'my other name', vote: 'G'}}}
global rooms
rooms = {}

# General routes
@app.route('/res/<path:path>')
def resource_serve(path):
    return send_from_directory('./res', path)

# User routes
@app.route('/', defaults={'room': ''})
@app.route('/r/<room>')
def index(room):
    room = room.lower()
    return render_template('index.html', room=room)

def init():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4().hex

@app.route('/ws/vote/<room>', methods=['POST', 'GET'])
def ws_set_vote(room):
    init()
    global rooms
    room = room.lower()
    if room not in rooms:
        rooms[room] = {}
    if request.method == 'POST':
        rooms[room][session['uuid']] = {'name': request.form.get('name', 'no name'), 'vote': request.form.get('vote', '')}
    if session['uuid'] in rooms[room]:
        return rooms[room][session['uuid']].get('vote', '')
    return ''

# Admin routes
@app.route('/admin', defaults={'room': ''})
@app.route('/admin/', defaults={'room': ''})
@app.route('/admin/<room>')
def admin(room):
    room = room.lower()
    return render_template('admin.html', room=room)

@app.route('/ws/admin/<room>')
def ws_admin(room):
    global rooms
    room = room.lower()
    if room not in rooms:
        rooms[room] = {}
    return json.dumps(rooms[room])

@app.route('/ws/reset/<room>')
def ws_reset(room):
    global rooms
    room = room.lower()
    rooms[room] = {}
    return 'ok'
