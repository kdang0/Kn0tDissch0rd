from live_chat import app,socketio
from live_chat.controllers import connection, receive, send

if __name__  == '__main__':
    socketio.run(app, debug=True)