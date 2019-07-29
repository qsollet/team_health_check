from flask import Flask, render_template, send_from_directory, session, request
import random
import json
import uuid
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aifk9042wkjefkj29e0fpowekjf!'

# rooms[questions{answers}] = {room_id: [{uuid_1: {name: 'my name', vote: 'A'}, uuid_2: {name: 'my other name', vote: 'G'}}]}
class Room():
    rooms = {}

    def __init__(self, name):
        self.name = name.lower()
        if self.name not in Room.rooms:
            Room.rooms[self.name] = {
                'current_question': 0,
                'votes': [{}]
            }

    def set_current_question(self, current_question):
        if current_question < 0:
            return 
        if len(Room.rooms[self.name]['votes']) <= current_question:
            for i in range(current_question + 1 - len(Room.rooms[self.name]['votes'])):
                Room.rooms[self.name]['votes'].append({})
        Room.rooms[self.name]['current_question'] = current_question

    def get_current_question(self):
        return Room.rooms[self.name]['current_question']

    def set_vote(self, user_id, username, vote):
        Room.rooms[self.name]['votes'][self.get_current_question()][user_id] = {'username': username, 'vote': vote}

    def get_vote(self, user_id):
        if user_id in Room.rooms[self.name]['votes'][self.get_current_question()]:
            return Room.rooms[self.name]['votes'][self.get_current_question()][user_id].get('vote', '')
        return ''

    def admin_get_results(self):
        return Room.rooms[self.name]

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
    r = Room(room.lower())
    if request.method == 'POST':
        r.set_vote(session['uuid'], request.form.get('name', 'no name'), request.form.get('vote', ''))
    return json.dumps({'vote': r.get_vote(session['uuid']), 'question': r.get_current_question()})

# Admin routes
@app.route('/admin', defaults={'room': ''})
@app.route('/admin/', defaults={'room': ''})
@app.route('/admin/r/<room>')
def admin(room):
    room = room.lower()
    return render_template('admin.html', room=room)

@app.route('/ws/admin/r/<room>')
def ws_admin(room):
    r = Room(room.lower())
    return json.dumps(r.admin_get_results())

@app.route('/ws/admin/set_q/<room>', methods=['POST', 'GET'])
def ws_set_question(room):
    if request.method == 'POST':
        r = Room(room.lower())
        r.set_current_question(int(request.form.get('index', '')))
    return 'ok'
