from live_chat import socketio
from flask_socketio import send, emit
from flask import render_template, request, session, redirect
from live_chat.models.user import User
from live_chat import app
from live_chat.models.room import Room
from live_chat.models.message import Message
from datetime import datetime
from flask_socketio import join_room, leave_room

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_rooms_joined({"id":session["user_id"]})
    rooms = Room.get_rooms_not_joined({"id":session["user_id"]})
    print("ROOMS:", rooms)
    if rooms and not user.rooms_joined:
        return render_template("home.html", available_rooms = rooms)
    return render_template("home.html", rooms= user.rooms_joined, available_rooms = rooms)

@app.route('/add_rm')
def add_rm():
    return render_template("add.html")

@app.route('/join', methods=["POST"])
def join():
    User.join({"room_id":request.form["room_id"], "user_id" : session["user_id"]})
    room = Room.get_one({"id": request.form["room_id"]})
    return redirect(f'/rm/{room.name}/{room.id}')


@app.route('/leave/<int:id>')
def leave(id):
    room = Room.get_one({"id" : id})
    if room.user_id == session['user_id']:
        User.leave({"room_id": id, "user_id" : session["user_id"]})
        Room.delete({"id" : id})
    User.leave({"room_id": id, "user_id" : session["user_id"]})
    return redirect('/home')

@app.route('/add', methods=["POST"])
def create():
    Room.save({"user_id":session['user_id'], "name":request.form["name"]})
    room = Room.recent_created({"user_id":session["user_id"]})
    User.join({"room_id":room.id, "user_id":session["user_id"]})
    return redirect(f'/rm/{room.name}/{room.id}')

@app.route('/rm/<string:name>/<int:id>')
def rm(name, id):
    rooms = User.get_rooms_joined({"id":session["user_id"]})
    users = Room.get_users_joined({"id":id})
    all_messages = Message.get_user_messages({"room_id" : id})            
    user = User.get_cur_user({"id" : session["user_id"]})
    print("length of list: ",len(users.users_joined))
    for user in users.users_joined:
        print("User's name",user.name)
    if all_messages:
        return render_template('room_chat.html', messages=all_messages,rooms=rooms.rooms_joined, users=users.users_joined,rm_id = id, rm_name = name, cur_user = user)
    return render_template('room_chat.html', rooms=rooms.rooms_joined, users=users.users_joined, rm_name = name, cur_user = user, rm_id = id)

@socketio.on("join_room")
def handle_join_room(data):
    join_room(f"{data['room_id']}")
    emit('join_room',data, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    msg_id = Message.save(
        {
            "message_content" : data["message_content"],
            "room_id" : data["room_id"],
            "user_id" : data["user_id"]
        })
    msg = Message.getOne({"id" : msg_id})
    msg_data = {
        "id" : msg.id,
        "user_name" : data["name"],
        "user_id" : data["user_id"],
        "content" : data["message_content"],
        "created_at" : msg.created_at.strftime('%m/%d/%Y, %#I:%M%p'),
        "updated_at" : msg.created_at.strftime('%m/%d/%Y, %#I:%M%p')
    }
    emit('send_message', msg_data, room=f"{data['room_id']}")

@socketio.on('load_messages')
def handle_load_messages(data):
    messages = Message.get_user_messages(data)
    json_messages = []
    for msg in messages:
        json_messages.append({
            "id" : msg.id,
            "user_id" : msg.user.id,
            "content" : msg.message_content,
            "created_at" :  msg.created_at.strftime('%m/%d/%Y, %#I:%M%p'),
            "updated_at" : msg.created_at.strftime('%m/%d/%Y, %#I:%M%p'),
            "user_name" : msg.user.name
        })
    emit('load_messages', {"messages" : json_messages}, json=True)