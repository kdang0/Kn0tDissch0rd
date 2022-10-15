from live_chat import socketio
from flask_socketio import send, emit
from flask import render_template
from live_chat import app

# @socketio.on('connect')
# def test_connect(auth):
#     print("We're connected")
#     emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route("/")
def index():
    return render_template("index.html")