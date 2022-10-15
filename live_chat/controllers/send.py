from flask_socketio import send, emit
from live_chat import socketio

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    send(message, broadcast = True)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)

