from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "MAKE IT MAKE SENSE"
socketio = SocketIO(app)
