from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "MAKE IT MAKE SENSE"
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
