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

@app.route('/', defaults={'room': ''.join(random.choices(string.ascii_lowercase, k=6))})
@app.route('/<room>')
def index(room):
    session['room'] = room
    return render_template('index.html', room=room)

@app.route('/admin/<room>/<key>')
def admin(room, key):
    session['room'] = room
    # TODO is a key really needed? if yes what to use?
    if key == 'aaa':
        return render_template('admin.html')
    return 'Not found', 404

@app.route('/img/<path:path>')
def img_serve(path):
    return send_from_directory('./img', path)

@app.route('/js/<path:path>')
def js_serve(path):
    return send_from_directory('./js', path)

def init():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4().hex

@app.route('/ws/vote', methods=['POST', 'GET'])
def ws_set_vote():
    init()
    global rooms
    if session['room'] not in rooms:
        rooms[session['room']] = {}
    if request.method == 'POST':
        rooms[session['room']][session['uuid']] = {'name': request.form.get('name', 'no name'), 'vote': request.form.get('vote', '')}
    if session['uuid'] in rooms[session['room']]:
        return rooms[session['room']][session['uuid']].get('vote', '')
    return ''

@app.route('/ws/admin/<key>')
def ws_admin(key):
    # Check the key
    if key != 'kuhfiosijfe':
        return 'Not found', 404
    global rooms
    if session['room'] not in rooms:
        rooms[session['room']] = {}
    return json.dumps(rooms[session['room']])

@app.route('/ws/reset/<key>')
def ws_reset(key):
    # Check the key
    if key != 'kuhfiosijfe':
        return 'Not found', 404
    global rooms
    rooms[session['room']] = {}
    return 'ok'
