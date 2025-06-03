from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
from datetime import datetime
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    chat_id = data['chat_id']
    sender = data['sender']
    join_room(chat_id)
    emit('joined', {'msg': f'{sender} joined room {chat_id}'}, room=chat_id)

@socketio.on('chat_message')
def handle_message(data):
    chat_id = data['chat_id']
    sender = data['sender']
    message = data['message']
    timestamp = datetime.now().strftime('%H:%M')
    emit('chat_message', {'sender': sender, 'message': message, 'time': timestamp}, room=chat_id)

@socketio.on('signal')
def handle_signal(data):
    chat_id = data['chat_id']
    data.pop('chat_id')
    emit('signal', data, room=chat_id, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
