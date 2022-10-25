from live_chat import socketio
from flask_socketio import send, emit
from flask import render_template, request, session, redirect
from live_chat.models.user import User
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
    return render_template("login.html")

@app.route("/registration")
def registration():
    return render_template("register.html")

@app.route('/login', methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    session['user_id'] = User.get_cur_user({"email" : request.form["email"]}).id
    return redirect('/home')

@app.route('/register', methods=["POST"])
def register():

    if not User.validate_registration(request.form):
        return redirect('/registration')
    data = {
        **request.form
    }
    User.save(data)
    session['user_id'] = User.get_cur_user({"email" : request.form["email"]}).id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')